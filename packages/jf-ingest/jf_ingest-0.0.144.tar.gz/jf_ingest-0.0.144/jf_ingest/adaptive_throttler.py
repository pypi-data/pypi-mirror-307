import inspect
import threading
import time
from contextlib import contextmanager
from typing import Any, Generator, Optional

from jf_ingest.logging_helper import logger, send_to_agent_log_file
from jf_ingest.telemetry.metrics import JellyCounter, JellyGauge, JellyHistogram


class AdaptiveThrottler:
    """
    Thread safe adaptive throttler that returns dynamically adjusts backoff times given a dataset and
    percentile threshold.
    """

    def __init__(
        self,
        max_rps: float = 10.0,
        baseline_window_size: int = 100,
        percentile_threshold: float = 0.95,
        backoff_factor: float = 0.85,
        reverse_backoff_factor: float = 0.95,
        reverse_backoff_counter: int = 25,
        logging_extra: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Initialize the adaptive throttler with the specified parameters.

        Args:
            max_rps: Maximum request rate allowed (requests per second).
            baseline_window_size: Number of response times to collect before establishing the baseline.
            percentile_threshold: The percentile of the baseline response times to use as the threshold.
            backoff_factor: Factor by which to decrease the request rate when response times exceed the threshold.
            reverse_backoff_factor: Factor by which to increase the request rate when response times are
                                    consistently below the threshold
            reverse_backoff_counter: Number of consecutive responses within the threshold to trigger a slight
                                     relaxation of the backoff factor.
            logging_extra: Extra logging information to include in the log messages
        """

        # Max RPS is the maximum request rate allowed. If the baseline RPS is higher than this,
        # throttle based on the max_rps instead. This ensures that the minimum backoff time is
        # significant enough to prevent overloading the server.
        self.max_rps = max_rps

        # Backoff factor is the degree to which the backoff rate is increased when the response
        # time exceeds the threshold. For example, if the backoff factor is 0.75, the backoff rate
        # will be increased by 25% each time the response time exceeds the threshold.
        self.backoff_factor = backoff_factor

        # Reverse backoff factor is the degree to which the backoff rate is decreased when the
        # response time is consistently below the threshold. For example, if the reverse backoff
        # factor is 0.95, the backoff rate will be decreased by 5% each time the response time is
        # consistently below the threshold
        self.reverse_backoff_factor = reverse_backoff_factor

        # Reverse backoff counter is the number of consecutive responses within the threshold that
        # will trigger a slight relaxation of the backoff factor. This is useful for gradually
        # increasing the request rate when (inferred) server load returns to normal.
        self.reverse_backoff_counter = reverse_backoff_counter

        # Window size is the number of response times to collect before establishing the baseline.
        # A larger window size will provide a more accurate baseline, but will take longer to
        # establish and is at risk of treating quick increases in server load as normal.
        # A smaller window size will establish the baseline more quickly, but may be less accurate.
        self._window_size = baseline_window_size

        # Percentile threshold is the percentile of the baseline response times to use as the
        # incoming response time threshold.
        self._percentile_threshold = percentile_threshold

        # Request rate is the dynamically adjusted request rate based on the baseline response times.
        # Backoff times are calculated based on this rate. This variable is adjusted based on the backoff
        # factor and reverse backoff factor when the response time exceeds or is below the threshold.
        self._request_rate: float = 0.0

        # Initial request rate is the initial request rate calculated based on the baseline response.
        # This variable does not change once set, and is used for comparison with the dynamically adjusted
        # request rate.
        self._initial_request_rate: float = 0.0

        # Percentile threshold time is the calculated response time at the specified percentile of the
        # baseline response times. This is used as the threshold for incoming response times.
        self._percentile_threshold_time: float = 0.0

        # Response times is a list of response times used to establish the baseline.
        self._response_times: list[float] = []

        # Response within threshold counter is the counter of consecutive recorded responses within
        # the threshold.
        self._response_within_threshold_counter = 0

        self.logging_extra: dict[str, Any] = {}
        self.metrics_attrs: dict[str, Any] = {}

        if logging_extra:
            self.logging_extra = logging_extra

            for k in ["company_slug", "function_name"]:
                if v := logging_extra.get(k):
                    self.metrics_attrs = {k: v}

        self._lock = threading.Lock()

        # Initialize metrics
        self._response_time_histogram = JellyHistogram(
            name="jf_ingest_adaptive_throttler_response_times",
            unit="s",
            description="Response times observed by AdaptiveThrottler",
        )

        self._request_rate_gauge = JellyGauge(name="jf_ingest_adaptive_throttler_request_rate")

        self._backoff_counter = JellyCounter(
            name="jf_ingest_adaptive_throttler_backoff_events",
            description="Number of times backoff was applied in AdaptiveThrottler",
        )

        self._reverse_backoff_counter = JellyCounter(
            name="jf_ingest_adaptive_throttler_reverse_backoff_events",
            description="Number of times reverse backoff was applied in AdaptiveThrottler",
        )

        self._backoff_time_histogram = JellyHistogram(
            name="jf_ingest_adaptive_throttler_backoff_times",
            unit="s",
            description="Backoff times applied by AdaptiveThrottler",
        )

        self._total_requests_counter = JellyCounter(
            name="jf_ingest_adaptive_throttler_total_requests",
            description="Total number of requests processed by AdaptiveThrottler",
        )

    def _record_response_time(self, response_time: float) -> None:
        """Record response time for establishing the baseline."""
        self._response_times.append(response_time)

        if len(self._response_times) == self._window_size:
            self._compute_percentile()
            self._calculate_dynamic_rate()

    def _compute_percentile(self) -> None:
        """Compute the specified percentile of the baseline response times."""
        sorted_times = sorted(self._response_times)
        i = int(self._percentile_threshold * len(sorted_times))
        self._percentile_threshold_time = sorted_times[i]

        msg_prefix = f"{self._percentile_threshold}th percentile response time calculated"
        send_to_agent_log_file(
            f"{msg_prefix}: {self._percentile_threshold_time:.4f} seconds",
            extra=self.logging_extra,
        )

    def _calculate_dynamic_rate(self) -> None:
        """Calculate the initial request rate dynamically based on the baseline response times."""
        average_time = sum(self._response_times) / len(self._response_times)
        rr = min(1 / average_time, self.max_rps)
        self._request_rate, self._initial_request_rate = rr, rr
        send_to_agent_log_file(
            f"Dynamic initial request rate calculated: {rr:.4f} rps",
            extra=self.logging_extra,
        )
        self._request_rate_gauge.measure(value=self._request_rate, attributes=self.metrics_attrs)

    @contextmanager
    def process_response_time(self) -> Generator[None, None, None]:
        """
        Context manager that records the duration of code execution within the 'with' block,
        processes the response time, and applies backoff if required.

        Usage:
            with adaptive_throttler.process_response_time():
                # Code to execute and measure
        """
        if not self.metrics_attrs.get("function_name"):
            current_frame = inspect.currentframe()

            if current_frame and current_frame.f_back and current_frame.f_back.f_back:
                caller_frame = current_frame.f_back.f_back
                f_name = caller_frame.f_code.co_name
                send_to_agent_log_file(
                    f"Adaptive throttler called from {f_name}", extra=self.logging_extra
                )
            else:
                send_to_agent_log_file(
                    "Adaptive throttler called from unknown function", extra=self.logging_extra
                )
                f_name = "unknown"

            self.metrics_attrs["function_name"] = f_name
            self.logging_extra["function_name"] = f_name

        start_time = time.perf_counter()

        try:
            yield
        finally:
            end_time = time.perf_counter()
            response_time = end_time - start_time

            with self._lock:
                self._response_time_histogram.measure(
                    value=response_time, attributes=self.metrics_attrs
                )
                self._total_requests_counter.add(amount=1, attributes=self.metrics_attrs)

                if len(self._response_times) < self._window_size:
                    self._record_response_time(response_time)
                    return

                # If the response time exceeds the threshold, decrease the request rate
                # and apply the backoff time
                if (
                    self._percentile_threshold_time
                    and response_time > self._percentile_threshold_time
                ):
                    self._request_rate *= self.backoff_factor
                    self._response_within_threshold_counter = 0

                    backoff_time = 1 / self._request_rate
                    send_to_agent_log_file(
                        f"Request rate decreased to {self._request_rate:.4f} rps, waiting {backoff_time:.4f} seconds",
                        extra=self.logging_extra,
                    )

                    self._request_rate_gauge.measure(
                        value=self._request_rate, attributes=self.metrics_attrs
                    )
                    self._backoff_counter.add(amount=1, attributes=self.metrics_attrs)
                    self._backoff_time_histogram.measure(value=backoff_time)

                    time.sleep(backoff_time)
                elif self._request_rate < self._initial_request_rate:
                    self._response_within_threshold_counter += 1

                    # If there have been enough consecutive responses within the threshold, slightly
                    # relax the backoff factor
                    if self._response_within_threshold_counter == self.reverse_backoff_counter:
                        self._request_rate = min(
                            self._request_rate / self.reverse_backoff_factor,
                            self._initial_request_rate,
                        )
                        self._response_within_threshold_counter = 0

                        self._request_rate_gauge.measure(
                            value=self._request_rate, attributes=self.metrics_attrs
                        )
                        self._reverse_backoff_counter.add(amount=1, attributes=self.metrics_attrs)

                        send_to_agent_log_file(
                            f"Request rate increased to {self._request_rate:.4f} rps",
                            extra=self.logging_extra,
                        )
