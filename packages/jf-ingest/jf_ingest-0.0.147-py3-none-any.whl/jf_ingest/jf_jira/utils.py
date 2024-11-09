from typing import Optional

import requests

from jf_ingest.utils import (
    get_jellyfish_api_base_url,
    get_jellyfish_api_token,
    retry_for_status,
)


def get_jellyfish_jira_issues_count(
    jellyfish_api_base_url: Optional[str] = None, jellyfish_api_token: Optional[str] = None
) -> int:
    """Helper function for getting the total number of issues that exist in Jellyfish

    Args:
        jellyfish_api_base_url (Optional[str]): Used as the base API to get data from jellyfish. If not provided, we will attempt to read it from the global variable.
        jellyfish_api_token (Optional[str]): Used for authenticating against Jellyfish. If not provided, we will attempt to read it from the global variable.

    Returns:
        int: The total number of Jellyfish Jira Issues that exist in this customers instance
    """
    if not jellyfish_api_base_url:
        jellyfish_api_base_url = get_jellyfish_api_base_url()
    if not jellyfish_api_token:
        jellyfish_api_token = get_jellyfish_api_token()

    base_url = jellyfish_api_base_url
    headers = {"Jellyfish-API-Token": jellyfish_api_token}

    r = retry_for_status(
        requests.get,
        f"{base_url}/endpoints/jira/issues/count",
        headers=headers,
    )
    r.raise_for_status()
    json_resp: dict = r.json()
    num_issues: int = json_resp.get('total_issues_in_jellyfish', 0)

    return num_issues
