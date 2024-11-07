import json
import logging
import math
import string
import threading
from collections import defaultdict
from contextlib import AbstractContextManager, nullcontext
from datetime import datetime, timezone
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Union,
)

import pytz
from jira import JIRA, JIRAError, Project
from requests import Response

from jf_ingest import diagnostics, logging_helper
from jf_ingest.adaptive_throttler import AdaptiveThrottler
from jf_ingest.config import IssueListDiff, IssueMetadata
from jf_ingest.constants import Constants
from jf_ingest.jf_jira.exceptions import (
    NoAccessibleProjectsException,
    NoJiraUsersFoundException,
)
from jf_ingest.telemetry import add_telemetry_fields, jelly_trace, record_span
from jf_ingest.utils import (
    DEFAULT_HTTP_CODES_TO_RETRY_ON,
    PROJECT_HTTP_CODES_TO_RETRY_ON,
    RetryLimitExceeded,
    ThreadPoolWithTqdm,
    batch_iterable,
    format_date_to_jql,
    retry_for_status,
    tqdm_to_logger,
)

logger = logging.getLogger(__name__)


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_fields(
    jira_connection: JIRA,
    include_fields: list[str] = [],
    exclude_fields: list[str] = [],
) -> list[dict]:
    """Download JIRA Fields from the fields API endpoint

    Args:
        jira_connection (JIRA): A Jira Connection Object
        include_fields (list[str], optional): A List of fields to exclusively include. Defaults to [].
        exclude_fields (list[str], optional): A list of fields to exclude. Defaults to [].

    Returns:
        list[dict]: A list of raw JIRA Field Objects
    """
    logger.info("Downloading Jira Fields... ")

    filters = []
    if include_fields:
        filters.append(lambda field: field["id"] in include_fields)
    if exclude_fields:
        filters.append(lambda field: field["id"] not in exclude_fields)

    fields = [
        field for field in jira_connection.fields() if all(filter(field) for filter in filters)
    ]

    logger.info(f"Done downloading Jira Fields! Found {len(fields)} fields")
    return fields


def _detect_project_rekeys_and_update_metadata(
    projects: list[Project],
    jellyfish_project_ids_to_keys: dict[str, str],
    jellyfish_issue_metadata: list[IssueMetadata],
) -> None:
    """Detects if a project has been rekeyed, and marks all related issue data as needs to be redownloaded.

    It marks the issues as needing to be redownloaded by setting their 'updated' field to datetime.min!

    Args:
        projects (list[Project]): A list of JIRA Project objects
        jellyfish_project_ids_to_keys (dict[str, str]): A lookup table for getting jira project IDs to Keys. Necesarry because a project KEY can change but it's ID never does
        jellyfish_issue_metadata (dict[str, dict]): A list of issue metadata from our database. Used to mark issues for potential redownload
    """
    rekeyed_projects = []
    for project in projects:
        # Detect if this project has potentially been rekeyed !
        if (
            project.id in jellyfish_project_ids_to_keys
            and project.raw["key"] != jellyfish_project_ids_to_keys[project.id]
        ):
            logging_helper.send_to_agent_log_file(
                f'Project (project_id={project.id}) {project.raw["key"]} was detected as being rekeyed (it was previously {jellyfish_project_ids_to_keys[project.id]}. Attempting to re-download all related jira issue data'
            )
            rekeyed_projects.append(project.id)

    # Mark issues for redownload if they are associated with rekeyed projects
    for metadata in jellyfish_issue_metadata:
        if metadata.project_id in rekeyed_projects:
            # Updating the updated time for each issue will force a redownload
            metadata.updated = pytz.utc.localize(datetime.min)


def _get_project_filters(
    include_projects: list[str],
    exclude_projects: list[str],
    include_categories: list[str],
    exclude_categories: list[str],
) -> list:
    filters = []
    if include_projects:
        filters.append(lambda proj: proj.key in include_projects)
    if exclude_projects:
        filters.append(lambda proj: proj.key not in exclude_projects)
    if include_categories:

        def _include_filter(proj):
            # If we have a category-based allowlist and the project
            # does not have a category, do not include it.
            if not hasattr(proj, "projectCategory"):
                return False

            return proj.projectCategory.name in include_categories

        filters.append(_include_filter)

    if exclude_categories:

        def _exclude_filter(proj):
            # If we have a category-based excludelist and the project
            # does not have a category, include it.
            if not hasattr(proj, "projectCategory"):
                return True

            return proj.projectCategory.name not in exclude_categories

        filters.append(_exclude_filter)
    return filters


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_projects_and_versions_and_components(
    jira_connection: JIRA,
    is_agent_run: bool,
    jellyfish_project_ids_to_keys: dict[str, str],
    jellyfish_issue_metadata: list[IssueMetadata],
    include_projects: list[str],
    exclude_projects: list[str],
    include_categories: list[str],
    exclude_categories: list[str],
) -> list[dict]:
    """Download Project Versions and Components

    Hits three separate APIs (projects, versions, and components)
    and squashes all of the data into one list of Project Data

    Args:
        jira_connection (JIRA): A Jira Connection Object
        is_agent_run (bool): A boolean flag that represents if the current run is an agent run
        jellyfish_project_ids_to_keys (dict[str, str]): A lookup table of Jellyfish Project IDs to Keys. Used for detecting rekeys
        jellyfish_issue_metadata (dict[str,dict]): A list of jellyfish issue metadata. Used to potentially mark issues as needing a redownload
        include_projects (list[str]): A list of projects to include exclusively
        exclude_projects (list[str]): A list of projects and exclude
        include_categories (list[str]): A list of categories to determine which projects to exclusively include
        exclude_categories (list[str]): A list of categories to determine which potential projects to exclude

    Raises:
        NoAccessibleProjectsException: Raise an exception if we cannot connect to a project

    Returns:
        list[dict]: A list of projects that includes Versions and Component data
    """
    with record_span('download_jira_projects'):
        logger.info("Downloading Jira Projects...")
        filters: list = (
            _get_project_filters(
                include_projects=include_projects,
                exclude_projects=exclude_projects,
                include_categories=include_categories,
                exclude_categories=exclude_categories,
            )
            if is_agent_run
            else []
        )

        all_projects: list[Project] = retry_for_status(
            jira_connection.projects, statuses_to_retry=PROJECT_HTTP_CODES_TO_RETRY_ON
        )

        projects = [proj for proj in all_projects if all(filt(proj) for filt in filters)]

        if not projects:
            raise NoAccessibleProjectsException(
                "No Jira projects found that meet all the provided filters for project and project category. Aborting... "
            )
        add_telemetry_fields({'jira_project_count': len(projects)})

        _detect_project_rekeys_and_update_metadata(
            projects=projects,
            jellyfish_project_ids_to_keys=jellyfish_project_ids_to_keys,
            jellyfish_issue_metadata=jellyfish_issue_metadata,
        )

        logger.info("Done downloading Projects!")

    with record_span('download_jira_components'):
        logger.info("Downloading Jira Project Components...")
        component_count = 0
        for p in projects:
            components = [
                c.raw
                for c in retry_for_status(
                    jira_connection.project_components,
                    p,
                    statuses_to_retry=PROJECT_HTTP_CODES_TO_RETRY_ON,
                )
            ]
            p.raw.update({"components": components})
            component_count += len(components)
        add_telemetry_fields({'jira_project_component_count': component_count})
        logger.info("Done downloading Project Components!")

    with record_span('download_jira_versions'):
        logger.info("Downloading Jira Versions...")
        result: list[dict] = []
        version_count = 0
        for p in projects:
            versions = retry_for_status(
                jira_connection.project_versions,
                p,
                statuses_to_retry=PROJECT_HTTP_CODES_TO_RETRY_ON,
            )
            p.raw.update({"versions": [v.raw for v in versions]})
            result.append(p.raw)
            version_count += len(versions)
        add_telemetry_fields({'jira_project_version_count': version_count})
        logger.info("Done downloading Jira Versions!")

    logger.info(
        f"Done downloading Jira Project, Components, and Version. Found {len(result)} projects"
    )
    return result


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_users(
    jira_basic_connection: JIRA,
    jira_atlas_connect_connection: JIRA,  # Set this to NONE for Agent
    gdpr_active: bool,
    search_users_by_letter_email_domain: Optional[str] = None,  # Direct connect related Field
    required_email_domains: list[str] = [],  # Agent related field
    is_email_required: bool = False,  # Agent related Field
    using_connect_as_primary_auth: bool = False,
) -> list[dict]:
    """Download Jira Users to memory

    Args:
        jira_basic_connection (JIRA): A Jira connection authenticated with Basic Auth. Should NEVER be set to None!
        jira_atlas_connect_connection (JIRA): A Jira connection authenticated with Atlassian Direct Connect. Should be set to None
        when working with Agent or for specific instances in M.I.
        gdpr_active (bool): A boolean flag that represents if the client is Jira Server or Jira Cloud. If gdpr_active is False than the client is on Jira Server. For Jira Server clients we search for user data via _search_by_letter
        search_users_by_letter_email_domain (str, optional): Something set on Jira Instances (M.I.) that narrows down
        the search results when using _search_users_by_letter. ONLY APPLICABLE WITH JIRA SERVER INSTANCES. Defaults to None.
        required_email_domains (list[str], optional): Used by Agent, set up in the config.yml file. Used to filter for only specific users that we care about. Defaults to None.
        is_email_required (str, optional): When provided, if we are filtering by email domains (with required_email_domains) than this field WILL INCLUDE emails that have a null email field!!! Beware: counter intuitive!. Defaults to None.
        using_connect_as_primary_auth (bool, optional): If True, we are using Atlassian Connect for connections by default. Defaults to False.

    Returns:
        list[dict]: A list of raw jira users, augmented with emails
    """
    logger.info("Downloading Users...")
    jira_users = search_users(
        jira_connection=jira_basic_connection,
        gdpr_active=gdpr_active,
        search_users_by_letter_email_domain=search_users_by_letter_email_domain,
        using_connect_as_primary_auth=using_connect_as_primary_auth,
    )

    # Fetching user email requires Atlassian Connect connection
    if jira_atlas_connect_connection:
        jira_users = [
            u for u in augment_jira_user_with_email(jira_atlas_connect_connection, jira_users)
        ]
    else:
        # If we don't have emails, we don't need to record the date at
        # which we pulled them.
        for u in jira_users:
            u["email_pulled"] = None

    jira_users = _scrub_jira_users(jira_users, required_email_domains, is_email_required)

    if len(jira_users) == 0:
        raise NoJiraUsersFoundException(
            'We are unable to see any users. Please verify that this user has the "browse all users" permission.'
        )

    add_telemetry_fields({'jira_user_count': len(jira_users)})

    logger.info(f"Done downloading Users! Found {len(jira_users)} users")
    return jira_users


def search_users(
    jira_connection: JIRA,
    gdpr_active: bool,
    search_users_by_letter_email_domain: Optional[str] = None,
    page_size: int = 1000,
    using_connect_as_primary_auth: bool = False,
) -> list[dict]:
    """Handler for searching for users. IF GDPR is active, we use a good API endpoint. If GDPR is not active,
    we do a crazy 'search all letters' approach, because of a known bug in JIRA Server instances (https://jira.atlassian.com/browse/JRASERVER-65089)

    Args:
        jira_connection (JIRA): A Jira connection (Basic Auth)
        gdpr_active (bool): If True, we are on Jira Cloud (use the good API). If False, we use the painful _search_by_letter_approach
        search_users_by_letter_email_domain (str, optional): For Server only. Allows us to narrow down search results. Defaults to None.
        page_size (int, optional): _description_. Defaults to 1000.
        using_connect_as_primary_auth (bool, optional): If True, we are using Atlassian Connect for connections by default. Defaults to False.

    Raises:
        NoJiraUsersFoundException: _description_

    Returns:
        _type_: A list of raw jira users
    """
    if gdpr_active and not using_connect_as_primary_auth:
        jira_users = _get_all_users_for_gdpr_active_instance(
            jira_connection=jira_connection, page_size=page_size
        )
    else:
        jira_users = _search_users_by_letter(
            jira_connection=jira_connection,
            gdpr_active=gdpr_active,
            search_users_by_letter_email_domain=search_users_by_letter_email_domain,
            page_size=page_size,
            using_connect_as_primary_auth=using_connect_as_primary_auth,
        )

    logging_helper.send_to_agent_log_file(f"found {len(jira_users)} users")
    return jira_users


def _jira_user_key(user_dict: dict, gdpr_active: bool = False, **kwargs) -> str:
    """Helper function used for getting unique set of users

    Args:
        user_dict (dict): Raw User dict from JIRA API
        gdpr_active (bool, optional): Switches what key to grab, depending on if we are server or cloud. Defaults to False.

    Raises:
        KeyError: _description_

    Returns:
        _type_: Jira User Unique key (accountId or Key, depending on gdpr_active)
    """

    # Choose the key name based on the GDPR status
    if gdpr_active:
        key_name = "accountId"
    else:
        key_name = "key"

    # Return a default value if one is provided, otherwise raise a KeyError
    try:
        if "default" in kwargs:
            default_value = kwargs["default"]
            kn: str = user_dict.get(key_name, default_value)
        else:
            kn = user_dict[key_name]

        return kn
    except KeyError as e:
        raise KeyError(
            f'Error extracting user data from Jira data. GDPR set to "{gdpr_active}" and expecting key name: "{key_name}" in user_dict. This is most likely an issue with how the GDPR flag is set on Jira instance. If this is a Jira Agent configuration, the agent config.yml settings may also be wrong.'
        ) from e


def get_searchable_jira_letters() -> list[str]:
    """Returns a list of lowercase ascii letters and all digits. DOES NOT INCLUDE PUNCTUATION!!!

    Note from Noah 6/28/22 - when using _search_users_by_letter with at least some
    jira server instances, some strange behavior occurs, explained with an example:
    take a case where search_users_by_letter_email_domain is set to '@business.com'
    meaning the query for the letter 'a' will be 'a@business.com'. Jira appears to
    take this query and split it on the punctuation and symbols, e.g [a, business, com].
    It then searches users username, name, and emailAddress for matches, performing the
    same punctuation and symbol split, and looking for matches starting at the beginning
    of each string, e.g. anna@business.com is split into [anna, business, com] and matches,
    but barry@business.com, split into [barry, business, com] will not match. Notably,
    these splits can match multiple substrings, which can lead to large lists of users.
    For example, when searching on the letter c, the full query would be 'c@business.com'
    split into [c, business, com]. This would obviously match cam@business.com, following
    the pattern from before, but unfortunately, the 'c' in the query will match any email
    ending in 'com', so effectively we will download every user. This will occur for
    letters matching every part of the variable search_users_by_letter_email_domain, split
    on punctuation and symbols.
    Notably, this will also happen when search_users_by_letter_email_domain is not set but
    there is still an overlap in the query and email address, e.g. query 'b' would hit all
    users in this hypothetical instance with an '@business.com' email address, since jira
    will split that address and search for strings starting with that query, matching b to business.
    In the future, this domain searching could provide a faster way than searching every
    letter to get all users for instances that have that variable set, but for the time
    being it requires pagination when searching by letter.


    Returns:
        list[str]: A list of lowercase ascii letters and all digits
    """
    return [*string.ascii_lowercase, *string.digits]


def _search_by_users_by_letter_helper(
    jira_connection: JIRA,
    base_query: str,
    search_users_by_letter_email_domain: Optional[str] = None,
    max_results: int = 1000,
    using_connect_as_primary_auth: bool = False,
) -> list[dict]:
    """This is both a recursive and iterative function for searching for users on GDPR non compliant instances.
    It works by searching for each letter/number in the ascii set (get_searchable_jira_letters). If we find there
    are more than 1000 values for a letter, we will page for more results for that letter.

    IF we find that we can get exactly 1000 results for a letter and nothing more, that means we've likely hit
    this jira bug: https://jira.atlassian.com/browse/JRASERVER-65089. The work around for this scenario is to
    recursively iterate on THE NEXT letters that we want to search on. For example, if we are searching for the
    letter 'a', and we get exactly 1000 results than we would recurse on this function with the following queries:
    'aa', 'ab', 'ac', 'ad'... until we no longer run into this error

    Args:
        jira_connection (JIRA): _description_
        base_query (str): _description_
        search_users_by_letter_email_domain (str, optional): _description_. Defaults to None.
        max_results (int, optional): _description_. Defaults to 1000.
        using_connect_as_primary_auth (bool, optional): If True, we are using Atlassian Connect for connections by default. Defaults to False.

    Returns:
        list[dict]: A list of raw user objects
    """
    users: list[dict] = []
    for letter in get_searchable_jira_letters():
        start_at = 0
        query_iteration = f"{base_query}{letter}"
        query_to_search = (
            f"{query_iteration}@{search_users_by_letter_email_domain}"
            if search_users_by_letter_email_domain
            else f"{query_iteration}"
        )
        total_found_for_current_iter = 0
        while True:
            payload: dict[str, Union[str, int, bool]] = {
                "startAt": start_at,
                "maxResults": max_results,
                "includeActive": True,
                "includeInactive": True,
            }
            if not using_connect_as_primary_auth:
                payload["username"] = query_to_search
            else:
                payload["query"] = query_to_search

            users_page: list[dict] = jira_connection._get_json("user/search", payload)
            users.extend(users_page)
            total_found_for_current_iter += len(users_page)

            # IF we get back a full page for a letter, than we need to refire I query.
            # Example: if we get 1000 users for the letter 'b', than we need to search
            # for ba, bb, bc, bd, etc.
            # Following work around from here: https://jira.atlassian.com/browse/JRASERVER-65089
            if not users_page and start_at == max_results:
                logger.info(
                    f"Jira bug relating to only getting limited (10, 100, or 1000) results per page hit when querying for {query_to_search} encountered. "
                    f"Specifically it looks like we have found {total_found_for_current_iter} results for {query_to_search}"
                    "Recursing on this function to search for more user results"
                )
                users.extend(
                    _search_by_users_by_letter_helper(
                        jira_connection=jira_connection,
                        base_query=query_iteration,
                        search_users_by_letter_email_domain=search_users_by_letter_email_domain,
                        max_results=max_results,
                    )
                )
                break
            elif not users_page:
                break
            else:
                start_at += len(users_page)

    return users


def _search_users_by_letter(
    jira_connection: JIRA,
    gdpr_active: bool,
    search_users_by_letter_email_domain: Optional[str] = None,
    page_size: int = 1000,
    using_connect_as_primary_auth: bool = False,
) -> list[dict]:
    """Search the 'old' API with each letter in the alphabet. Only used for non-GDPR compliant servers or apps using Connect-based auth.

    Args:
        jira_connection (JIRA): Basic Jira Connection
        gdpr_active (bool): A boolean flag that represents if the client is Jira Server or Jira Cloud. If gdpr_active is False than the client is on Jira Server. For Jira Server clients we search for user data via _search_by_letter
        search_users_by_letter_email_domain (str, optional): If provided, email domain will be used to narrow down the list of returned users from the API. Defaults to None.
        page_size (int, optional): _description_. Defaults to 1000.
        using_connect_as_primary_auth (bool, optional): If True, we are using Atlassian Connect for connections by default. Defaults to False.

    Returns:
        _type_: _description_
    """
    non_deduped_jira_users: list[dict] = []
    if search_users_by_letter_email_domain and not gdpr_active:
        # NOTE: search_users_by_letter_email_domain doing searches by email domain
        # only works for Jira Servers (which should always have gdpr_active set to False)
        # support multiple domains via comma separated list
        for domain in search_users_by_letter_email_domain.split(","):
            if not domain:
                continue
            non_deduped_jira_users.extend(
                _search_by_users_by_letter_helper(
                    jira_connection=jira_connection,
                    base_query="",
                    search_users_by_letter_email_domain=domain,
                    max_results=page_size,
                    using_connect_as_primary_auth=using_connect_as_primary_auth,
                )
            )
    else:
        non_deduped_jira_users = _search_by_users_by_letter_helper(
            jira_connection=jira_connection,
            base_query="",
            max_results=page_size,
            using_connect_as_primary_auth=using_connect_as_primary_auth,
        )
    jira_users_dict = {
        _jira_user_key(u, using_connect_as_primary_auth): u for u in non_deduped_jira_users
    }

    return list(jira_users_dict.values())


def _get_all_users_for_gdpr_active_instance(
    jira_connection: JIRA,
    page_size=1000,
) -> list[dict]:
    """Gets ALL users from JIRA API. This includes active and inactive. Leverages
    the "Get All Users" API endpoint:
    https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-users/#api-rest-api-2-users-search-get

    Args:
        jira_connection (JIRA): Jira Connection
        max_results (int, optional): Total number of users per page. Defaults to 1000.

    Returns:
        _type_: Returns unique list of all Jira Users in the Jira instance
    """
    jira_users: dict[str, dict] = {}
    start_at = 0

    # Fetch users one page at a time
    while True:
        users = retry_for_status(
            jira_connection._get_json,
            "users/search",
            {
                "startAt": start_at,
                "maxResults": page_size,
            },
        )

        jira_users.update({_jira_user_key(u, gdpr_active=True): u for u in users})

        if len(users) == 0:
            break  # no need to keep paging
        else:
            start_at += len(users)

    return list(jira_users.values())


def _scrub_jira_users(
    jira_users: list[dict], required_email_domains: list[str], is_email_required: bool
) -> list[dict]:
    """Helper function for removing users we want to ignore. This is used predominantly by the agent as of 10/30/23

    Args:
        jira_users (list): _description_
        required_email_domains (list[str]): _description_
        is_email_required (bool): _description_
    """

    def _get_email_domain(email: str):
        try:
            return email.split("@")[1]
        except AttributeError:
            return ""
        except IndexError:
            return ""

    filtered_users: list[dict] = []
    required_email_domains_lowered = [
        email_domain.lower() for email_domain in required_email_domains
    ]
    for user in jira_users:
        """
        Scrubs external jira users in-place by overwriting 'displayName' and 'emailAddress' fields
        See OJ-5558 for more info.
        """
        if "accountType" in user and user["accountType"] == "customer":
            user["displayName"] = "EXTERNAL"
            user["emailAddress"] = ""

        # Filter out unwanted emails
        # (Agent use case)
        if required_email_domains_lowered:
            try:
                email = user["emailAddress"]
                email_domain = _get_email_domain(email)
                if email_domain.lower() in required_email_domains_lowered:
                    filtered_users.append(user)
            except KeyError:
                # NOTE: This was introduced in the Agent awhile ago
                # and honestly it seems like a bug from a UX perspective.
                # The comment around this functionality (see example.yml)
                # implies that this statement should really be 'if not is_email_required'
                # Switching this without doing any research could cause a flood
                # of bad user data to get ingested, though, so we'd need to do a careful
                # analysis of who has this flag set and work with them to straighten it out.
                # Pain.
                if is_email_required:
                    filtered_users.append(user)
        else:
            filtered_users.append(user)

    return filtered_users


def _should_augment_email(user: dict) -> bool:
    """Helper function for determing if a user should be augmented

    Args:
        user (dict): Raw user Object

    Returns:
        bool: Boolean (true if we SHOULD augment a user)
    """
    # if we don't have an accountId, or we got an email already,
    # then this instance isn't GPDR-ified; just use what we've got
    email = user.get("emailAddress")
    account_id = user.get("accountId")
    account_type = user.get("accountType")

    if email or not account_id:
        return False

    # OJ-6900: Skip Jira users that are of type "customer". These
    # are not particularly useful to Jellyfish (they are part of
    # Jira Service Desk) so skip fetching emails for them.
    elif account_type == "customer":
        return False

    return True


def augment_jira_user_with_email(
    jira_atlassian_connect_connection: JIRA, jira_users: list
) -> Iterator[dict[str, Union[str, datetime]]]:
    """Attempts to augment a raw user object with an email, pulled from the
    atlassian direct connect JIRA connection. IF we do augment a user, we
    will add a new dictionary key to the raw user called 'email_pulled', which
    represents a UTC datetime of when we used the atlassian direct connect API.
    We need this timestamp to submit reports to Atlassian of when we used this
    API endpoint, see: https://developer.atlassian.com/cloud/jira/platform/user-privacy-developer-guide/#reporting-user-personal-data-for-your-apps

    Args:
        jira_atlassian_connect_connection (JIRA): A connection to Atlassian via their AtlassianConnect authentication
        jira_users (list): A list of raw users

    Yields:
        dict: A list of raw users with the 'email_pulled' key added, as well as their 'emailAddress' key potentially updated
    """

    for u in tqdm_to_logger(jira_users, desc="augmenting users with emails..."):
        account_id = u.get("accountId")
        u["email_pulled"] = None
        if not _should_augment_email(u):
            yield u
        else:
            # hit the email API to retrieve an email for this user
            try:
                u["emailAddress"] = jira_atlassian_connect_connection._get_json(
                    "user/email", params={"accountId": account_id}
                )["email"]
                u["email_pulled"] = datetime.now(timezone.utc)
            except JIRAError as e:
                # 404s are normal; don't log them
                if getattr(e, "status_code", 0) != 404:
                    logging_helper.send_to_agent_log_file(
                        f"Error retrieving email for {account_id}, skipping...",
                        level=logging.WARNING,
                    )
            yield u


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_resolutions(jira_connection: JIRA) -> list[dict]:
    """Downloads Jira Resolution objects

    Args:
        jira_connection (JIRA): A Jira connection object

    Returns:
        list[dict]: The raw Resolution objects
    """
    logger.info("Downloading Jira Resolutions...")
    try:
        result = [r.raw for r in retry_for_status(jira_connection.resolutions)]
        logger.info(f"Done downloading Jira Resolutions! Found {len(result)} resolutions")
        return result
    except Exception as e:
        logger.warning(f'Error downloading resolutions, got {e}')
        return []


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issuetypes(
    jira_connection: JIRA,
    project_ids: list[str],
) -> list[dict]:
    """
    For Jira next-gen projects, issue types can be scoped to projects.
    For issue types that are scoped to projects, only extract the ones
    in the included projects (by project_ids).

    Args:
        jira_connection (JIRA): Jira Connection
        project_ids (list[str]): List of Project IDs to include, if we
        are dealing with a 'next-gen' Jira Project

    Returns:
        list[dict]: List of Raw Issue Types pulled direct from Jira API
    """
    logger.info(
        "Downloading IssueTypes...",
    )
    result: list[dict] = []
    for it in retry_for_status(jira_connection.issue_types):
        if "scope" in it.raw and it.raw["scope"]["type"] == "PROJECT":
            if it.raw["scope"]["project"]["id"] in project_ids:
                result.append(it.raw)
        else:
            result.append(it.raw)
    logger.info(f"Done downloading IssueTypes! found {len(result)} Issue Types")
    return result


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issuelinktypes(jira_connection: JIRA) -> list[dict]:
    """Download Jira Issue Link Types from the issueLinkType endpoint.

    Args:
        jira_connection (JIRA): A Jira connection, from the jira Python library

    Returns:
        list[dict]: A list of 'raw' JSON objects pulled directly from the issueLinkType endpoint
    """
    logger.info("Downloading IssueLinkTypes...")
    result = [lt.raw for lt in retry_for_status(jira_connection.issue_link_types)]
    logger.info(f"Done downloading IssueLinkTypes! Found {len(result)} Issue Link Types")
    return result


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_priorities(jira_connection: JIRA) -> list[dict]:
    """Loads Jira Priorities from their API. Has 429 handling logic

    Args:
        jira_connection (JIRA): A Jira connection (with the provided Jira Library)

    Returns:
        list[dict]: A list of 'raw' JSON objects pulled from the 'priority' endpoint
    """
    logger.info("Downloading Jira Priorities...")
    result = [p.raw for p in retry_for_status(jira_connection.priorities)]
    logger.info(f"Done downloading Jira Priorities! Found {len(result)} priorities")
    return result


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_boards_and_sprints(
    jira_connection: JIRA, download_sprints: bool
) -> tuple[list[dict], list[dict], list[dict]]:
    """Downloads boards and sprints. This function is pretty inefficient, mostly due
    to limitations of JIRA. To fetch every sprint, we have to fetch every board. To do so,
    we fetch every board then hit another API to get the sprints related to that board (which
    potentially involves paging for sprints on one board, or fetching NO sprints for that board)
    TODO: This could be sped up with parallelization, like we do with issues

    Args:
        jira_connection (JIRA): Jira Connection Object
        download_sprints (bool): Boolean representing if we should skip pulling sprints or not

    Returns:
        tuple[list[dict], list[dict], list[dict]]: This function returns three lists. The first list represents
        raw board data. The second list represents raw sprint data. The last list represents how sprints map to boards
    """
    b_start_at = 0
    b_batch_size = 50
    all_jira_boards = []

    with record_span('download_jira_boards'):
        logger.info(f"Downloading Boards...")
        while True:
            jira_boards = retry_for_status(
                jira_connection.boards, startAt=b_start_at, maxResults=b_batch_size
            )
            if not jira_boards:
                break
            b_start_at += len(jira_boards)
            all_jira_boards.extend([b.raw for b in jira_boards])
        add_telemetry_fields({'jira_board_count': len(all_jira_boards)})
        logger.info(f"Done downloading Boards! Found {len(all_jira_boards)} boards")

    all_sprints = []
    links = []
    with record_span('download_sprints'):
        if download_sprints:
            # We're seeing a weird potentially transient issues with some jira servers
            # serving us a 401 on some sprint API calls. We can't reproduce it consistently,
            # so we should add 401s to the retry process for now
            retry_for_statuses = list(DEFAULT_HTTP_CODES_TO_RETRY_ON) + [401]
            for board in tqdm_to_logger(
                all_jira_boards,
                total=len(all_jira_boards),
                desc="Downloading Sprints...",
            ):
                sprints_for_board = []
                s_start_at = 0
                s_batch_size = 50
                board_id = board["id"]
                while True:
                    # create sprints, if necessary
                    board_sprints_page = None
                    try:
                        board_sprints_page = retry_for_status(
                            jira_connection.sprints,
                            board_id=board_id,
                            startAt=s_start_at,
                            maxResults=s_batch_size,
                            statuses_to_retry=retry_for_statuses,
                        )
                    except JIRAError as e:
                        if e.status_code == 400:
                            logging_helper.send_to_agent_log_file(
                                f"Board ID {board_id} (project {board['name']}) doesn't support sprints -- skipping"
                            )
                        else:
                            # JIRA returns 500, 404, and 503s errors for various reasons: board is
                            # misconfigured; "failed to execute search"; etc.  Just
                            # skip and move on for all JIRAErrors
                            logger.warning(
                                f"Couldn't get sprints for board {board_id} (HTTP Error Code {e.status_code})"
                            )
                    except RetryLimitExceeded as e:
                        logger.warning(
                            f'Retry limit exceeded when attempting to pull sprints for board {board_id}. Error: {e}'
                        )

                    if not board_sprints_page:
                        break

                    sprints_for_board.extend(board_sprints_page)
                    s_start_at += len(board_sprints_page)

                all_sprints.extend(sprints_for_board)
                links.append(
                    {"board_id": board_id, "sprint_ids": [s.id for s in sprints_for_board]}
                )
        add_telemetry_fields({'jira_sprint_count': len(all_sprints)})

    return all_jira_boards, [s.raw for s in all_sprints], links


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issues_from_new_sync(
    jira_connection: JIRA,
    issue_download_concurrent_threads: int,
    jira_issues_batch_size: int,
    issue_ids_to_download: set[str],
    include_fields: list[str],
    exclude_fields: list[str],
) -> Generator[dict, None, None]:
    """
    Downloads all issues raw issues that we need and yields them as dictionaries.
    This will use the "new sync" method, that detects rekeys and deletes using 10k issue batch
    sizes.

    Args:
        jira_connection (JIRA): A valid Jira Connection
        issue_download_concurrent_threads (int): The number of threads we can hit the API with
        jira_issues_batch_size (int): The batch size for downloading raw issues. This is generally 100 for cloud and 250 for server. It can be configured on the jellyfish side of the house.
        issue_ids_to_download (set[str]): A set of Jira IDs (as strings) to re-download.
        include_fields (list[str]): A list of fields to include in the raw issues
        exclude_fields (list[str]): A list of fields to exclude in the raw issues

    Yields:
        Generator[dict, None, None]: This YIELDS raw dictionaries, which represent raw Issue data from JIRA
    """
    #######################################################################
    # Pull Jira Issues
    #######################################################################

    logger.info(f'{len(issue_ids_to_download)} issue IDs have been marked as needing download')

    logger.info(f"Attempting to pull {len(issue_ids_to_download)} full issues")

    # This returns a GENERATOR for issues
    return pull_jira_issues_by_jira_ids(  # type: ignore
        jira_connection=jira_connection,
        jira_ids=issue_ids_to_download,
        num_parallel_threads=issue_download_concurrent_threads,
        batch_size=jira_issues_batch_size,
        expand_fields=["renderedFields", "changelog"],
        include_fields=include_fields,
        exclude_fields=exclude_fields,
    )


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issues(
    jira_connection: JIRA,
    full_redownload: bool,
    issue_download_concurrent_threads: int,
    jira_issues_batch_size: int,
    issue_metadata_from_jellyfish: list[IssueMetadata],
    issue_metadata_from_jira: list[IssueMetadata],
    include_fields: list[str],
    exclude_fields: list[str],
) -> Generator[dict, None, None]:
    """Download all Jira Issues based on a 'pull_from' date, and a set of
    metadata from our database, and a list of projects are are concerned with.
    Uses a threadpool, with a variable number of workers

    If you need to pull just a set of Issues see pull_jira_issues_by_jira_ids
    If you need to pull all issues by project key and datetime, see pull_all_jira_issues_by_date

    Args:
        jira_connection (JIRA): A JIRA connection object
        jira_projects (list[str]): A list of Jira Projects by Key
        full_redownload (bool): boolean flag to force a full redownload or not
        issue_download_concurrent_threads (int): The number of threads to use in the ThreadPoolExecutor
        jira_issues_batch_size (int): The batch size we should use for hitting the JIRA API for issues
        issue_metadata_from_jellyfish (list[IssueMetadata]): A list of Jellyfish Issue Metadata, useful for
        determining if we already have issues or if issues got deleted
        issue_metadata_from_jira (list[IssueMetadata]): A list of Jira Issue Metadata, useful for
        determining if we already have issues or if issues got deleted
        include_fields (list[str]): A list of optional fields that we want to exclusively have
        in each issue
        exclude_fields (list[str]): a list of fields we want to exclude from the jira issues we get back

    Returns:
        Generator[dict, None, None]: Returns a GENERATOR of raw issue (json) objects
    """

    #######################################################################
    # Pull Jira Issues
    #######################################################################

    # Next, detect which issues exist in Jira, but don't exist in our
    # system yet (inverse of above)
    missing_issue_ids = get_ids_from_difference_of_issue_metadata(
        source=issue_metadata_from_jira,
        dest=issue_metadata_from_jellyfish,
    )
    # Lastly, find issues that exist in both of our sets, but are
    # 'outdated' in our set
    out_of_date_issue_ids = get_out_of_date_issue_ids(
        issue_metadata_from_jira=issue_metadata_from_jira,
        issue_metadata_from_jellyfish=issue_metadata_from_jellyfish,
        full_redownload=full_redownload,
    )

    issue_ids_to_redownload = detect_issues_needing_re_download(
        issue_metadata_from_jira=issue_metadata_from_jira,
        issue_metadata_from_jellyfish=issue_metadata_from_jellyfish,
    )

    issue_ids_to_download = [
        *missing_issue_ids,
        *out_of_date_issue_ids,
        *issue_ids_to_redownload,
    ]

    logger.info(
        "Using IssueMetadata we have detected that "
        f"{len(missing_issue_ids)} issues are missing, "
        f"{len(out_of_date_issue_ids)} issues are out of date, "
        f"{len(issue_ids_to_redownload)} issues need to be redownloaded (because of rekey and parent relations), "
        f"for a total of {len(issue_ids_to_download)} issues to download"
    )

    logger.info(f"Attempting to pull {len(issue_ids_to_download)} full issues")

    # This returns a GENERATOR for issues
    return pull_jira_issues_by_jira_ids(  # type: ignore
        jira_connection=jira_connection,
        jira_ids=issue_ids_to_download,
        num_parallel_threads=issue_download_concurrent_threads,
        batch_size=jira_issues_batch_size,
        expand_fields=["renderedFields", "changelog"],
        include_fields=include_fields,
        exclude_fields=exclude_fields,
    )


def get_jira_results_looped(
    jira_connection: JIRA,
    jql_query: str,
    batch_size: int,
    issue_count: int,
    expand_fields: list[str] = [],
    include_fields: list[str] = [],
    exclude_fields: list[str] = [],
) -> list[dict]:
    """Get all issues from Jira using a JQL query. This function wraps _download_issue_page and loops until all pages have been fetched
    Args:
        jira_connection (JIRA): A JIRA connection object
        jql_query (str): A JQL query to fetch issues
        batch_size (int): The batch size to use when fetching issues
        issue_count (int): The total number of issues to fetch
        expand_fields (list[str]): A list of fields to expand
        include_fields (list[str]): A list of fields to include
        exclude_fields (list[str]): A list of fields to exclude
    Returns:
        A list of raw issue objects
    """
    total_results: list[dict] = []
    logging_helper.send_to_agent_log_file(
        f"Fetching {issue_count} issues in batches of {batch_size} using jql {jql_query}",
        level=logging.DEBUG,
    )
    start_at = 0
    while start_at < issue_count:
        results, total_to_fetch = _download_issue_page(
            jira_connection=jira_connection,
            jql_query=jql_query,
            start_at=start_at,
            batch_size=batch_size,
            expand_fields=expand_fields,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            return_total=True,
        )

        total_results.extend(results)
        start_at += len(results)
        # if the total to fetch is different than what we expected, update the progress bar
        if total_to_fetch != issue_count:
            issue_count = total_to_fetch  # type: ignore

    logging_helper.send_to_agent_log_file(
        f"Done fetching {issue_count} issues in batches of {batch_size} using jql {jql_query}. {len(total_results)} results found",
        level=logging.DEBUG,
    )
    return total_results


def fetch_id_to_key_for_all_existing(
    jira_connection: JIRA,
    project_ids: List[str],
    pull_from: datetime,
) -> Dict[str, str]:
    """Given our local IssueMetadata, fetch all issues from Jira and return a dictionary of id to key
    Args:
        jira_connection (JIRA): A JIRA connection object
        project_ids (list[str]): A list of project IDs
        pull_from: the pull_from date
    """

    id_to_key_on_remote = {}
    project_id_to_pull_from = {project_id: pull_from for project_id in project_ids}
    project_id_to_issue_count = _get_all_project_issue_counts(
        jira_connection=jira_connection,
        project_key_to_pull_from=project_id_to_pull_from,
        num_parallel_threads=10,
    )

    # Attempt to get maximum batch size for this "cheap" query. On Jira Cloud and most
    # Jira Servers we can go 10k at a time, but for some Jira Server's it limits us to 1000
    batch_size = get_jira_search_batch_size(
        jira_connection=jira_connection, optimistic_batch_size=10000, fields=['id', 'key']
    )
    logging_helper.send_to_agent_log_file(
        f'Attempting to pull Key and ID from remote Jira Source for all issues, using batch_size of {batch_size}'
    )
    for proj_id, proj_issue_count in project_id_to_issue_count.items():
        jql_expression = generate_project_pull_from_jql(project_key=proj_id, pull_from=pull_from)
        logging_helper.send_to_agent_log_file(
            f"Fetching all IDs for {proj_id} (batch_size={batch_size}, jql={jql_expression})",
            level=logging.DEBUG,
        )
        issue_id_to_key = get_jira_results_looped(
            jira_connection=jira_connection,
            jql_query=jql_expression,
            batch_size=batch_size,
            issue_count=proj_issue_count,
            include_fields=['id', 'key'],
        )
        id_to_key_on_remote.update({str(issue['id']): issue['key'] for issue in issue_id_to_key})

    return id_to_key_on_remote


def get_issue_ids_for_rekeys_and_deletes(
    jira_connection: JIRA,
    jellyfish_issue_metadata: list[IssueMetadata],
    project_key_to_id: dict[str, str],
    pull_from: datetime,
) -> IssueListDiff:
    """This is part of the "new sync" path, and this function is responsible for crawling
    over all remote Issue Key and IDs and detecting what has been deleted and what has been
    rekeyed. The subfunction that crawls over the API will query for 10k issues at a time.

    Args:
        jira_connection (JIRA): A valid Jira Connection
        jellyfish_issue_metadata (list[IssueMetadata]): A list of Issue meta data from Jellyfish
        project_key_to_id (dict[str, str]): A translation dictionary to get ID from Key (for Jira Projects)
        pull_from (datetime): The root pull from for this Jira Instance

    Returns:
        IssueListDiff: A named Tuple indicating what needs to get deleted and what needs to get downloaded
    """
    issue_ids_to_download: set[str] = set()

    logger.info("Processing projects and issues from remote")
    project_ids = list(project_key_to_id.values())

    if len(project_ids) == 0 and len(jellyfish_issue_metadata) > 0:
        logger.warning("No valid projects found in local metadata")

    logger.info(f"Fetching list of all jira issue ID/key from remote to match local")
    id_to_key_on_remote = fetch_id_to_key_for_all_existing(jira_connection, project_ids, pull_from)

    # Transform local issues to lookup table for ID to Key
    id_to_key_on_local = {str(issue.id): issue.key for issue in jellyfish_issue_metadata}

    # Get two unique sets for remote and local to compare to find things deleted in Jira
    ids_on_local = set([issue.id for issue in jellyfish_issue_metadata])
    ids_on_remote = set(id_to_key_on_remote.keys())

    # all deleted
    issue_ids_to_delete = ids_on_local.difference(ids_on_remote)
    logger.info(
        f"{len(id_to_key_on_local)} issues local, {len(id_to_key_on_remote)} issues remote, "
        f"{len(issue_ids_to_delete)} issues deleted"
    )

    # all changed key
    detected_rekey_count = 0
    for issue_id in id_to_key_on_local.keys():
        if (
            issue_id in id_to_key_on_remote
            and id_to_key_on_local[issue_id] != id_to_key_on_remote[issue_id]
        ):
            detected_rekey_count += 1
            issue_ids_to_download.add(issue_id)

    logger.info(
        f'{detected_rekey_count} issues have been detected as being rekeyed. These will be redownloaded'
    )

    # everything on remote in the pull_from window not on local is "new" but could have been deleted from local.
    issue_ids_to_create = ids_on_remote.difference(ids_on_local)
    logger.info(
        f"{len(issue_ids_to_create)} issues found on remote not found on local. These will be downloaded."
    )
    issue_ids_to_download.update(issue_ids_to_create)

    issue_list_for_download = IssueListDiff(
        ids_to_delete=issue_ids_to_delete, ids_to_download=issue_ids_to_download
    )

    add_telemetry_fields(
        {
            'jira_issue_ids_on_local': len(ids_on_local),
            'jira_issue_ids_on_remote': len(ids_on_remote),
            'jira_issue_ids_to_delete': len(issue_ids_to_delete),
            'jira_issue_ids_to_create': len(issue_ids_to_create),
            'jira_issue_ids_to_rekey': detected_rekey_count,
            'jira_issue_ids_to_download': len(issue_ids_to_download),
        }
    )

    return issue_list_for_download


def generate_project_pull_from_jql(project_key: str, pull_from: datetime) -> str:
    """Generates a JQL for a given project key and a pull from date

    Args:
        project_key (str): A project Key
        pull_from (datetime): A 'pull_from' date

    Returns:
        str: project = {project_key} AND updated > {format_date_to_jql(pull_from)} order by id asc
    """
    return f'project = "{project_key}" AND updatedDate > {format_date_to_jql(pull_from)} order by id asc'


def _get_all_project_issue_counts(
    jira_connection: JIRA,
    project_key_to_pull_from: dict[str, datetime],
    num_parallel_threads: int,
) -> dict[str, int]:
    """A helper function for quickly getting issue counts for each
    provided project. Filters against pull_from in it's JQL,
    and runs concurrently up to the num_parallel_threads value

    Args:
        jira_connection (JIRA): A Jira Connection object
        project_key_to_pull_from (dict[str, datetime]): A dictionary of Project Keys to Pull From
        num_parallel_threads (int): The total size of the thread pool to use

    Returns:
        dict[str, int]: A dictionary mapping the project key to it's issue count
    """
    project_key_to_issue_count: dict[str, int] = {}
    # Sanity check, do an early return if we don't have any project keys to pull from
    if len(project_key_to_pull_from) == 0:
        logging_helper.send_to_agent_log_file(
            msg='No project keys to pull from provided', level=logging.WARNING
        )
        return project_key_to_issue_count

    def _update_project_key_issue_count_dict(project_key: str, project_pull_from: datetime):
        project_key_to_issue_count[project_key] = _get_issue_count_for_jql(
            jira_connection=jira_connection,
            jql_query=generate_project_pull_from_jql(
                project_key=project_key, pull_from=project_pull_from
            ),
        )

    total_projects = len(project_key_to_pull_from)
    with ThreadPoolWithTqdm(
        desc=f"Getting total issue counts for {total_projects} projects (Thread Count: {num_parallel_threads})",
        total=total_projects,
        max_workers=num_parallel_threads,
    ) as pool:
        for project_key, project_pull_from in project_key_to_pull_from.items():
            pool.submit(
                _update_project_key_issue_count_dict,
                project_key=project_key,
                project_pull_from=project_pull_from,
            )

    return project_key_to_issue_count


def get_jira_search_batch_size(
    jira_connection: JIRA,
    optimistic_batch_size: int = Constants.MAX_ISSUE_API_BATCH_SIZE,
    fields: Iterable[str] = ('*all',),
) -> int:
    f"""A helper function that gives us the batch size that the
    JIRA provider wants to use. A lot of JIRA instances have their
    own batch sizes. Typically a JIRA SERVER will give us a batch size
    of 1000, but JIRA Cloud tends to limit us to 100. This function
    will attempt to get the highest reasonable batchsize possible.
    We've noticed some problems when querying for issues as high as
    1000, so we've limited the batch_size to be {Constants.MAX_ISSUE_API_BATCH_SIZE}

    Args:
        jira_connection (JIRA): A Jira Connection Object
        optimistic_batch_size (int, optional): An optimistic batch size. Defaults to {Constants.MAX_ISSUE_API_BATCH_SIZE}.
        fields ([Iterable[str]): A list of fields to include in the query. Defaults to ('*all',).

    Returns:
        int: The batchsize that JIRA is going to force us to use
    """
    max_res: int = _post_raw_result(
        jira_connection,
        jql_query="",
        fields=list(fields),
        expand=[],
        start_at=0,
        max_results=optimistic_batch_size,
    )['maxResults']
    return max_res


def _get_issue_count_for_jql(jira_connection: JIRA, jql_query: str) -> int:
    """Returns the total number of issues that we have access to via a given JQL

    Args:
        jira_connection (JIRA): A Jira Connection Object
        jql_query (str): A given JQL string that we want to test

    Returns:
        int: The total number of issues that the JQL will yield
    """
    try:
        total_issue_count: int = retry_for_status(
            jira_connection.search_issues,
            jql_query,
            startAt=0,
            fields="id",
            maxResults=1,  # Weird JIRA behavior, when you set max results to 0 it attempts to grab all issues
            json_result=True,
        )['total']
        return total_issue_count
    except JIRAError as e:
        if hasattr(e, "status_code") and 400 <= e.status_code < 500:
            logging_helper.send_to_agent_log_file(
                f"Exception when querying for JQL: {jql_query} - (HTTP ERROR {e.status_code}):\n{e}\nskipping...",
                level=logging.WARNING,
                exc_info=True,
            )
            return 0
        else:
            raise


def _expand_changelog(
    jira_connection: JIRA, jira_issues: list[dict], batch_size: int
) -> list[dict]:
    """Expands the change log for a given list of issues. Each Jira Issues has a page
    of changelogs, which is limited to roughly 50 items. If there are more than 50 items
    in the Jira instance, than we will need to page on that issue for the rest of the
    changelogs. This function is that paging logic

    Args:
        jira_connection (JIRA): A Jira Connection Object
        jira_issues (list[dict]): A list of JIRA Issue objects
        batch_size (int): The batchsize JIRA is going to restrict us to for paging

    Returns:
        list[dict]: The jira_issues that we received, but with the change log expanded
    """
    # HACK(asm,2024-07-25): The `issue/:issue_id/changelog` endpoint is only supported for Jira cloud
    server_info = jira_connection.server_info()
    if not server_info.get('deploymentType') == 'Cloud':
        return jira_issues

    for issue in jira_issues:
        changelog = issue.get("changelog")

        # If there is no changelog associated with the issue, there is nothing to expand
        if not changelog:
            continue

        # Happy path - we already have all changelog entries for this issue
        if changelog['total'] <= changelog['maxResults']:
            continue

        # If we have a changelog and there are more changelog entries to pull, grab them

        # NOTE(asm,2024-07-24): We discard the list of histories that are already on the issue
        # purposefully - the un-paginated list of histories are the most recent history entries, so
        # this loop repopulates them starting from the oldest history item.
        changelog['histories'] = list()

        # batch_size is usually defaulted to 250, which doesn't work properly with Jira cloud - use
        # whichever is smaller, the value the API tells us or the passed-in value.
        page_size = min(batch_size, changelog['maxResults'])
        for i in range(0, math.ceil(changelog['total'] / page_size)):
            more_changelogs = retry_for_status(
                jira_connection._get_json,
                f"issue/{issue['id']}/changelog",
                {"startAt": page_size * i, "maxResults": page_size},
            )["values"]
            changelog["histories"].extend(i for i in more_changelogs)
    return jira_issues


def _filter_changelogs(
    issues: list[dict], include_fields: list[str], exclude_fields: list[str]
) -> list[dict]:
    """The JIRA API will respect our include and exclude fields for top level
    issues, but it will often NOT respect it in it's historic data (changelog data).
    This function crawls all the change logs and scrubs out fields we do or do not
    want to have.

    Args:
        issues (list[dict]): A list of JIRA issues
        include_fields (list[str]): A list of fields we exclusively want
        exclude_fields (list[str]): A list of fields we want to scrub out

    Returns:
        list[dict]: A list of JIRA issues with a scrubbed changelog history
    """

    def _get_field_identifier(item) -> Optional[str]:
        return "fieldId" if "fieldId" in item else "field" if "field" in item else None

    cleaned_issues = []
    for issue in issues:
        if "changelog" in issue:
            changelog = issue["changelog"]
            if "histories" in changelog:
                histories = changelog["histories"]
                for history in histories:
                    cleaned_items = []
                    for item in history.get("items", []):
                        item_field_identifier = _get_field_identifier(item)

                        if not item_field_identifier:
                            logging_helper.log_standard_error(
                                level=logging.WARNING,
                                error_code=3082,
                                msg_args=[item.keys()],
                            )
                            continue
                        if include_fields and item.get(item_field_identifier) not in include_fields:
                            continue
                        if item.get(item_field_identifier) in exclude_fields:
                            continue
                        cleaned_items.append(item)

                    history["items"] = cleaned_items

        cleaned_issues.append(issue)

    return cleaned_issues


def _post_raw_result(
    jira_connection: JIRA,
    jql_query: str,
    fields: list[str],
    expand: list[str],
    start_at: int,
    max_results: int,
) -> dict:
    """Helper function for sending a POST call to the Jira API.
    To get around batch_size limitations in the JIRA python library,
    we do a POST command directly against the API endpoint. This allows
    us to throttle Jira as much as possible.
    This function is shared between get_issues_with_post, and
    get_jira_batch_size.

    Args:
        jira_connection (JIRA): A Jira Connection Object
        jql_query (str): A JQL query to hit the endpoint with
        fields (list[str]): The fields to get back
        expand (list[str]): The fields to expand
        start_at (int): The start at index
        max_results (int): The batch size to request

    Returns:
        Dict: A JSON objects. Technically this could be a list, but in practice I don't think it ever is.
    """
    response: Response = jira_connection._session.post(
        url=jira_connection._get_url('search'),
        data=json.dumps(
            {
                'jql': jql_query,
                'fields': fields,
                'expand': expand,
                'startAt': start_at,
                'maxResults': max_results,
            }
        ),
    )
    response.raise_for_status()
    r: dict = response.json()
    return r


def get_issues_with_post(
    jira_connection: JIRA,
    jql_query: str,
    fields: list[str],
    expand: list[str],
    start_at: int,
    max_results: int,
) -> tuple[list[str], str]:
    """This is a helper function that hits the JIRA API Search (issues) endpoint
    using POST instead of the library provided GET method. We need to use POST
    because sometimes for JIRA server we can hang indefinitely when using GET
    instead of POST, particularly when we are ingesting a very large issue

    Args:
        jira_connection (JIRA): A Jira connection Object
        jql_query (str): The JQL query to hit the API with
        fields (list[str]): The list of fields we want from the API
        expand (list[str]): The list of fields to expand
        start_at (int): The index to start at
        max_results (int): The maximum batch size to return. If the returned max_results value
        DOES NOT MATCH the requested, this will raise an error. "returned max_results" does not
        mean the total number of returned items; Jira returns us an accurate max_results of the
        total results it could return us, based on our query. To get the proper max_results to
        request with, you should first get the maximum batchsize this jira instance will allow
        for this query using get_jira_search_batch_size()

    Raises:
        A potential exception will get raised if you request with a batch_size that is too
        high for the Jira server to handle. To avoid this, please first use the get_jira_search_batch_size
        function to find the optimum batch_size to use

    Returns:
        tuple containing;
        - list[dict]: A list of issues in raw dictionary form
        - str representing the number of total issues for the jql query
    """
    json_response = _post_raw_result(
        jira_connection=jira_connection,
        jql_query=jql_query,
        fields=fields,
        expand=expand,
        start_at=start_at,
        max_results=max_results,
    )
    returned_max_results = json_response['maxResults']
    issues = json_response['issues']
    total_issues = json_response['total']
    if returned_max_results != max_results:
        raise Exception(
            f'JIRA maxResults does not match the requested maxResults ({max_results} != {returned_max_results})! '
            'This means that we are requesting a batch size that is too large! '
            f'start_at: {start_at}, request_max_results: {max_results}, '
            f'returned_max_results={returned_max_results}, total_issues: {total_issues}.'
        )
    return issues, total_issues


def _download_issue_page(
    jira_connection: JIRA,
    jql_query: str,
    start_at: int,
    batch_size: int,
    expand_fields: Optional[list[str]] = ["renderedFields", "changelog"],
    include_fields: list[str] = [],
    exclude_fields: list[str] = [],
    return_total: bool = False,
    adaptive_throttler: Optional[AdaptiveThrottler] = None,
) -> tuple[list[dict], int] | list[dict]:
    """Our main access point for getting JIRA issues. ALL functions responsible
    for fetching JIRA issues should leverage this helper function. This means
    that the function for fetching issues by date and issues by ID both funnel
    to this function

    This function leverages a bisecting search, to try to isolate problem issues
    in a given batch. It works by shrinking the batch size when we encounter an error,
    until we can isolate which JIRA issue(s) is giving us exceptions

    Args:
        jira_connection (JIRA): A JIRA connection object
        jql_query (str): The JQL we want to hit the API with
        start_at (int): The Start At value to use against the API
        batch_size (int): The batchsize that Jira forces us to use
        expand_fields (Optional[list[str]], optional): Fields we want to expand on the JIRA API. Defaults to ["renderedFields", "changelog"].
        include_fields (list[str], optional): A list of fields we want to exclusively use on the API. Defaults to [].
        exclude_fields (list[str], optional): A list of fields we want to scrub out. Defaults to [].
        return_total: default False but if True also return the total number of issues for a jql query (ie response.json()['total'] after pulling a segment)
        adaptive_throttler (Optional[AdaptiveThrottler], optional): An adaptive throttler object to use for rate limiting. Defaults to None.

    Returns:
        list[dict]: One BATCH of issues, and potentially the total number of issues for a jql query
    """
    changeable_batch_size = batch_size
    end_at = start_at + batch_size
    context_manager: Callable[..., AbstractContextManager]

    if adaptive_throttler:
        context_manager = adaptive_throttler.process_response_time
    else:
        context_manager = nullcontext

    while True:
        try:
            # Get Issues
            # NOTE: We use POST here because for some version of JIRA server
            # it is possible that it chokes up on large issues when using GET calls
            # (the jira library uses GET, so we need to interface with the session
            # object directly). See get_issues_with_post
            logging_helper.send_to_agent_log_file(
                f'{threading.get_native_id()} | started get_issues_with_post - {start_at=}',
                level=logging.DEBUG,
            )

            with context_manager():
                issues, total = retry_for_status(
                    get_issues_with_post,
                    jira_connection=jira_connection,
                    jql_query=jql_query,
                    # Note: we also rely on key, but the API 401s when
                    # asking for it explicitly, though it comes back anyway.
                    # So just ask for updated.
                    fields=get_fields_spec(
                        include_fields=include_fields, exclude_fields=exclude_fields
                    ),
                    expand=expand_fields,
                    start_at=start_at,
                    max_results=changeable_batch_size,
                )

            logging_helper.send_to_agent_log_file(
                f'{threading.get_native_id()} | finished get_issues_with_post - {start_at=}',
                level=logging.DEBUG,
            )
            # Potentially expand the changelogs
            issues = _expand_changelog(jira_connection, issues, batch_size)

            # Filter the changelogs
            issues_with_changelogs = _filter_changelogs(
                issues=issues,
                include_fields=include_fields,
                exclude_fields=exclude_fields,
            )
            if return_total:
                return issues_with_changelogs, total
            else:
                return issues_with_changelogs

        except Exception as e:
            logging_helper.send_to_agent_log_file(
                f'Exception encountered when attempting to get issue data. '
                f'start_at: {start_at}, end_at: {end_at}, batch_size: {batch_size}, error: {e}',
                level=logging.WARNING,
            )
            # DO NOT fail hard here. Attempt to shrink the batch size a few times (see blow)
            # and give up if we move the start_at cursor above the end_at marker
            if start_at > end_at:
                if return_total:
                    return [], 0
                else:
                    return []
            # We have seen sporadic server-side flakiness here. Sometimes Jira Server (but not
            # Jira Cloud as far as we've seen) will return a 200 response with an empty JSON
            # object instead of a JSON object with an "issues" key, which results in the
            # `search_issues()` function in the Jira library throwing a KeyError.
            #
            # Sometimes both cloud and server will return a 5xx.
            #
            # In either case, reduce the maxResults parameter and try again, on the theory that
            # a smaller ask will prevent the server from choking.
            if changeable_batch_size > 0:
                changeable_batch_size = int(
                    changeable_batch_size / 2
                )  # This will eventually lead to a batch size of 0 ( int(1 / 2) == 0 )
                logging_helper.send_to_agent_log_file(
                    f"Caught {type(e)} from search_issues(), reducing batch size to {changeable_batch_size}",
                    level=logging.WARNING,
                )

                if changeable_batch_size <= 0:
                    # Might be a transient error I guess, or might happen every time we request this specific
                    # issue. Either way, seems fine to ignore it. If a), we'll be able to fetch it again the
                    # next time we perform issue metadata downloading. If b), we'll never fetch this issue, but
                    # what else can we do? -- the Jira API never seems to be able to provide it to us.
                    logging_helper.send_to_agent_log_file(
                        f"Caught {type(e)} from search_issues(), batch size is already 0, giving up on "
                        f"fetching this issue's metadata. Args: jql_query={jql_query}, start_at={start_at}",
                        level=logging.WARNING,
                    )
                    start_at += 1
                    changeable_batch_size = batch_size


def generate_jql_for_batch_of_ids(id_batch: list[str]) -> str:
    """Generates a JQL to get a batch of IDs

    Args:
        id_batch (list[str]): A list of IDs

    Returns:
        str: A JQL of the following format: 'id in (1,2,3)'
    """
    try:
        return f'id in ({",".join(id_batch)}) order by id asc'
    except Exception as e:
        logger.error(f"Error generating JQL for batch of IDs: {id_batch}, got {e}")
        raise e


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def pull_jira_issues_by_jira_ids(
    jira_connection: JIRA,
    jira_ids: list[str] | set[str],
    num_parallel_threads: int,
    batch_size: int,
    expand_fields: Optional[list[str]] = [],
    include_fields: Optional[list[str]] = [],
    exclude_fields: Optional[list[str]] = [],
    hide_tqdm: Optional[bool] = False,
    adaptive_throttler: Optional[AdaptiveThrottler] = None,
) -> Generator[dict[str, Any], None, None]:
    """Fetches Issues based on a set of Issue IDs that we want to pull.
    This function deals with all of the paging and concurrency stuff we
    want to do to optimize our JIRA Issue ingestion

    Args:
        jira_connection (JIRA): A JIRA Connection object
        jira_ids (list[str]): A list of JIRA IDs
        num_parallel_threads (int): The number of threads to use in the ThreadPoolExecutor object
        batch_size (int): The Batch Size that JIRA will limit us to
        expand_fields (Optional[list[str]], optional): A list of fields we want to expand. Defaults to [].
        include_fields (Optional[list[str]], optional): A list of fields we want to exclusively pull. Defaults to [].
        exclude_fields (Optional[list[str]], optional): A list of fields we want to exclude. Defaults to [].
        hide_tqdm (Optional[bool], optional): A flag to hide the tqdm progress bar. Defaults to False.
        adaptive_throttler (Optional[AdaptiveThrottler], optional): An adaptive throttler object to throttle requests.

    Returns:
        Generator[dict, None, None]: A generator of raw Issues, which should yield the number of jira_ids provided
    """
    encountered_issue_ids = set()
    if not jira_ids:
        return

    with ThreadPoolWithTqdm(
        desc=f"Pulling issue data for {len(jira_ids)} Jira Issue IDs (Thread Count: {num_parallel_threads})",
        total=len(jira_ids),
        max_workers=num_parallel_threads,
        hide_tqdm=hide_tqdm,
    ) as pool:
        for issue_batch in batch_iterable(jira_ids, batch_size=batch_size):
            jql_query = generate_jql_for_batch_of_ids(issue_batch)
            pool.submit(
                _download_issue_page,
                jira_connection=jira_connection,
                jql_query=jql_query,
                start_at=0,
                batch_size=batch_size,
                expand_fields=expand_fields,
                include_fields=include_fields,
                exclude_fields=exclude_fields,
                adaptive_throttler=adaptive_throttler,
            )

        for issue_batch in pool.get_results():
            for issue in issue_batch:
                issue_id = issue['id']
                if issue_id not in encountered_issue_ids:
                    encountered_issue_ids.add(issue_id)
                    yield issue


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def pull_all_jira_issues_by_date(
    jira_connection: JIRA,
    project_key_to_pull_from: dict[str, datetime],
    num_parallel_threads: int,
    batch_size: int,
    expand_fields: Optional[list[str]] = [],
    include_fields: Optional[list[str]] = [],
    exclude_fields: Optional[list[str]] = [],
) -> Generator[dict, None, None]:
    """Fetch a list of IDs by searching for all issues in a given list of
    projects that have had their 'updated' field updated after the provided
    pull_from

    Args:
        jira_connection (JIRA): A Jira Connection object
        project_keys (list[str]): A list of project keys representing the projects we want to pull from
        pull_from (datetime): A 'pull_from' value, to pull issues that have their updated field as AFTER this argument
        num_parallel_threads (int): The number of thread we want to use in the ThreadPoolExecutor object
        batch_size (int): The batch size that JIRA is limiting us to
        expand_fields (Optional[list[str]], optional): A list of API fields that we want to expand. Defaults to [].
        include_fields (Optional[list[str]], optional): A list of fields we want to exclusively fetch. Defaults to [].
        exclude_fields (Optional[list[str]], optional): A list of fields we want to exclude. Defaults to [].

    Returns:
        list[dict]: A list of JIRA Issues that are within the requested projects that have been updated since the pull_from arg
    """
    # First, do a parallelized check across all projects to see
    # if they have issues or not
    project_issue_count_map = _get_all_project_issue_counts(
        jira_connection=jira_connection,
        project_key_to_pull_from=project_key_to_pull_from,
        num_parallel_threads=num_parallel_threads,
    )

    # Iterate across each project and fetch issue metadata based on
    # our date filtering
    project_key_to_found_issues: dict[str, list[dict]] = {}
    total_expected_issues: int = sum([count for count in project_issue_count_map.values()])

    with ThreadPoolWithTqdm(
        desc=f"Pulling issue data across {len(project_issue_count_map)} projects by Date (Thread Count: {num_parallel_threads})",
        total=total_expected_issues,
        max_workers=num_parallel_threads,
    ) as pool:
        for project_key, count in project_issue_count_map.items():
            project_key_to_found_issues[project_key] = []
            project_pull_from = project_key_to_pull_from[project_key]
            if count == 0:
                continue

            jql_query = generate_project_pull_from_jql(
                project_key=project_key, pull_from=project_pull_from
            )

            logging_helper.send_to_agent_log_file(
                f'Attempting to query for {count} issues with batch size {batch_size} using the following JQL: {jql_query}',
                level=logging.INFO,
            )
            for start_at in range(0, count, batch_size):
                pool.submit(
                    _download_issue_page,
                    jira_connection=jira_connection,
                    jql_query=jql_query,
                    start_at=start_at,
                    batch_size=batch_size,
                    expand_fields=expand_fields,
                    include_fields=include_fields,
                    exclude_fields=exclude_fields,
                )

            # Empty thread pool for each project, in attempt to keep
            # memory usage low in the threadpool
            for issue_batch in pool.get_results():
                for issue in issue_batch:
                    yield issue


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_all_issue_metadata(
    jira_connection: JIRA,
    project_keys: list[str],
    pull_from: datetime,
    num_parallel_threads: int,
    batch_size: int,
    recursively_download_parents: Optional[bool] = False,
) -> list[IssueMetadata]:
    """A function to grab all issue meta data, based on a pull from date (pull_from).
    This function pulls all issues that have been updated since the pull_from value,
    as well as their parents even if they haven't been updated since their pull from date.
    We MUST grab parents, even if they haven't been updated since the pull from date, because
    it is VERY bad for Jitis if we pull relevant issues but fail to ingest their parents

    Args:
        jira_connection (JIRA): A Jira Connection Object
        project_keys (list[str]): A list of projects to pull issue metadata for
        pull_from (datetime): A 'pull from' date, to use as a JQL filter
        num_parallel_threads (int): The number of threads we can parallelize with
        batch_size (int): The batch size that the JIRA instance is limiting us to
        recursively_download_parents (bool): When set to True, fetch all parents of parents, until we've searched all parent relations. Defaults to False.

    Returns:
        list[IssueMetadata]: A list of IssueMetadata objects that reflects all issues
        that exist in the company's Jira Instance
    """
    # Fetch all issue data by a provided date (pull_from)
    logger.info(
        f"Attempting to pull issue metadata for {len(project_keys)} projects, with a pull from date set as {pull_from}"
    )
    project_key_to_pull_from = {project_key: pull_from for project_key in project_keys}
    issues_by_date: list[dict] = list(
        pull_all_jira_issues_by_date(
            jira_connection=jira_connection,
            project_key_to_pull_from=project_key_to_pull_from,
            include_fields=["id", "key", "parent", "updated"],
            num_parallel_threads=num_parallel_threads,
            batch_size=batch_size,
        )
    )

    # Transform fetched issues into IssueMetadata
    issue_metadata_by_date_set: Set[IssueMetadata] = set(
        IssueMetadata.init_from_jira_issues(issues_by_date)
    )

    issue_meta_data_ids = set([issue_metadata.id for issue_metadata in issue_metadata_by_date_set])

    # Once we get all of the issue meta data within our date filter, there is
    # a chance that we are missing PARENT data that has somehow changed without
    # marking the 'updated' field in JQL (because the JIRA is bad). To get passed
    # this, we need to query for all parent IDs from the issues we found.
    # For Jellyfish JITIs purposes we generally do NOT need parent of parents, i.e. we don't need to
    # recursively query on parents. However, some clients need to fetch a large number of initiatives
    # that are the eventual-parents of all issues, which we can fetch with an optional bool provided (recursively_download_parents)
    missing_parent_id_set: Set[str] = set(
        [
            issue_metadata.parent_id
            for issue_metadata in issue_metadata_by_date_set
            if issue_metadata.parent_id and issue_metadata.parent_id not in issue_meta_data_ids
        ]
    )

    if not missing_parent_id_set:
        # Log if we never enter the loop, for potential debugging purposes
        logger.info(
            f"There were no detected missing parent issues. Not pulling any missing parent issues"
        )

    # Track depth level of loop for logging/debugging purposes
    depth_level = 1
    # Track all IDs we've seen to avoid loops/improve efficiency
    all_seen_ids = set()
    all_seen_ids.update(issue_meta_data_ids)
    all_seen_ids.update(missing_parent_id_set)
    # Track ALL parents in this set
    parent_issue_metadata = set()
    while missing_parent_id_set:
        logger.info(
            f"Attempting to pull metadata for an additional {len(missing_parent_id_set)} issues, which represents issue parents that we need to potentially redownload. (Parent Search Depth = {depth_level})"
        )
        parent_issues = [
            i
            for i in pull_jira_issues_by_jira_ids(
                jira_connection=jira_connection,
                jira_ids=missing_parent_id_set,
                num_parallel_threads=num_parallel_threads,
                batch_size=batch_size,
                include_fields=["id", "key", "parent", "updated"],
            )
        ]
        parent_issue_metadata_batch = set(
            IssueMetadata.init_from_jira_issues(parent_issues, skip_parent_data=False)
        )
        parent_issue_metadata.update(parent_issue_metadata_batch)
        all_seen_ids.update(
            set([_issue_metadata.id for _issue_metadata in parent_issue_metadata_batch])
        )

        if not recursively_download_parents:
            logger.info(
                f'Only grabbing the first level of parents, because recursively_download_parents is {recursively_download_parents}'
            )
            break

        # Now, since recursively_download_parents is true, we have to crawl across this issue of parents and grab THEIR parents
        missing_parent_id_set = set(
            [
                _issue_metadata.parent_id
                for _issue_metadata in parent_issue_metadata_batch
                if _issue_metadata.parent_id and _issue_metadata.parent_id not in all_seen_ids
            ]
        )
        depth_level += 1

    all_issue_meta_data = issue_metadata_by_date_set.union(parent_issue_metadata)

    logging_helper.send_to_agent_log_file(
        f"Found {len(issue_metadata_by_date_set)} issues by datetime filter (pull from: {pull_from}) "
        f"and another {len(parent_issue_metadata)} by fetching additional parent data for a total of "
        f"{len(all_issue_meta_data)} issue meta data"
    )
    return list(all_issue_meta_data)


def get_out_of_date_issue_ids(
    issue_metadata_from_jira: list[IssueMetadata],
    issue_metadata_from_jellyfish: list[IssueMetadata],
    full_redownload: bool,
) -> set[str]:
    """Helper function to determine what issues are 'out of date'. Out of date issues
    are issues that don't have a matching datetime value in our system.
    NOTE: When we want to redownload an issue, we set it's updated field to datetime.min!

    Args:
        issue_metadata_from_jira (list[IssueMetadata]): A list of issue metadata from Jellyfish
        issue_metadata_from_jellyfish (list[IssueMetadata]): A list of issue metadata pulled from Jira
        full_redownload (bool): _description_

    Returns:
        set[str]: A set of IDs that represent issues that are 'out of date'
    """
    out_of_date_jira_ids: list[str] = []
    jellyfish_ids_to_updated_date: dict[str, datetime] = {
        issue_metadata.id: issue_metadata.updated
        for issue_metadata in issue_metadata_from_jellyfish
    }
    jira_ids_to_updated_date: dict[str, datetime] = {
        issue_metadata.id: issue_metadata.updated for issue_metadata in issue_metadata_from_jira
    }

    for id, jf_updated in jellyfish_ids_to_updated_date.items():
        jira_updated = jira_ids_to_updated_date.get(id, None)
        if jira_updated and jira_updated > jf_updated or full_redownload:
            out_of_date_jira_ids.append(id)

    return set(out_of_date_jira_ids)


def get_ids_from_difference_of_issue_metadata(
    source: list[IssueMetadata],
    dest: list[IssueMetadata],
) -> set[str]:
    """Returns a set of Issue IDs that exist in source but not dest

    Args:
        source (list[IssueMetadata]): The left hand operand of the difference
        dest (list[IssueMetadata]): The right hand operand of the difference

    Returns:
        set[str]: source - dest
    """
    source_set = set(source)
    dest_set = set(dest)

    difference = source_set - dest_set

    return set([issue_metadata.id for issue_metadata in difference])


def detect_issues_needing_re_download(
    issue_metadata_from_jira: list[IssueMetadata],
    issue_metadata_from_jellyfish: list[IssueMetadata],
) -> list[str]:
    """Detects which issues need to be redownloaded because they have a
    dependency on an issue that we have detected as being rekeyed.

    Example:

    Issue ID 1 has had it's issue key changed from PROJ-1 to NEWPROJ-1
    Issues 2 and 3 have Issue 1 linked as a parent object
    Since Issue 1 has changed and needs to be redownloaded, Issues 2 and 3
    have to be redownloaded TOO, to fix the linkage/dependency they have on issue 1

    Args:
        issue_metadata_from_jira (list[IssueMetadata]): A list of issue metadata from JIRA
        issue_metadata_from_jellyfish (list[IssueMetadata]): A list of issue metadata from our database

    Returns:
        list[str]: A list of IDs that we need to redownload
    """
    issue_keys_changed: list[str] = []
    jf_issue_metadata_lookup = {
        issue_metadata.id: issue_metadata for issue_metadata in issue_metadata_from_jellyfish
    }

    for remote_metadata in issue_metadata_from_jira:
        jf_metadata = jf_issue_metadata_lookup.get(remote_metadata.id)
        if jf_metadata and remote_metadata.key != jf_metadata.key:
            logger.info(
                f"Detected a key change for issue {remote_metadata.id} ({jf_metadata.key} -> {remote_metadata.key})",
            )
            issue_keys_changed.append(jf_metadata.key)

    issues_by_epic_link_field_issue_key, issues_by_parent_field_issue_key = (
        defaultdict(list),
        defaultdict(list),
    )

    for issue_id, jf_issue_metadata in jf_issue_metadata_lookup.items():
        epic_link_field_issue_key = jf_issue_metadata.epic_link_field_issue_key
        parent_field_issue_key = jf_issue_metadata.parent_field_issue_key
        if jf_issue_metadata.epic_link_field_issue_key:
            issues_by_epic_link_field_issue_key[epic_link_field_issue_key].append(issue_id)
        if parent_field_issue_key:
            issues_by_parent_field_issue_key[parent_field_issue_key].append(issue_id)

    # Find all of the issues that refer to those issues through epic_link_field_issue_key
    # or parent_field_issue_key; these issues need to be re-downloaded
    issue_ids_needing_re_download = set()
    for changed_key in issue_keys_changed:
        issue_ids_needing_re_download.update(
            set(issues_by_epic_link_field_issue_key.get(changed_key, []))
        )
        issue_ids_needing_re_download.update(
            set(issues_by_parent_field_issue_key.get(changed_key, []))
        )

    return list(issue_ids_needing_re_download)


def get_fields_spec(include_fields: list[str] = [], exclude_fields: list[str] = []) -> list[str]:
    """A helper function to get a JIRA API friendly string for filtering against fields

    Args:
        include_fields (list[str], optional): A list of fields we want to exclusively use. Defaults to [].
        exclude_fields (list[str], optional): A list of fields that we want to exclude. Defaults to [].

    Returns:
        list[str]: A list of fields to pull. If include_fields and exclude_fields are both empty,
        we will return ['*all'] (return all fields)
    """
    field_spec = include_fields or ["*all"]
    field_spec.extend(f"-{field}" for field in exclude_fields)
    return field_spec


def _convert_datetime_to_worklog_timestamp(since: datetime) -> int:
    """Convert a datetime to a timestamp value, to be used for worklog querying

    Args:
        since (datetime): A datetime object

    Returns:
        int: An int, representing a unix timestamp that JIRA will accept on the worklogs API endpoint
    """
    try:
        timestamp = since.timestamp()
    except (AttributeError, ValueError):
        timestamp = 0
    updated_since = int(timestamp * 1000)
    return updated_since


# Returns a dict with two items: 'existing' gives a list of all worklogs
# that currently exist; 'deleted' gives the list of worklogs that
# existed at some point previously, but have since been deleted
@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit(logger)
def download_worklogs(
    jira_connection: JIRA, issue_ids: list[str], since: datetime
) -> dict[str, Union[list[dict], list[str]]]:
    """Returns a dict with two items: 'existing' give a list of all worklogs that currently
    exist; 'deleted' gives the list of worklog IDs that existed at some point previously, but
    have since been deleted

    Args:
        jira_connection (JIRA): A jira connection object
        issue_ids (list[str]): A list of issue IDs we are concerned with
        since (datetime): A datetime to 'pull from'

    Returns:
        dict[str, list]: Schema: {'updated': [...], 'deleted': [...]}
    """
    logger.info("Downloading Jira Worklogs...")
    updated: list[dict] = []
    deleted_ids: list[str] = []
    since_timestamp = _convert_datetime_to_worklog_timestamp(since)
    updated_since = since_timestamp
    deleted_since = since_timestamp

    logger.info("Fetching updated worklogs")
    while True:
        worklog_ids_json = retry_for_status(
            jira_connection._get_json,
            "worklog/updated",
            params={"since": updated_since},
        )
        updated_worklog_ids = [v["worklogId"] for v in worklog_ids_json["values"]]

        # The provided JIRA library does not support a 'worklog list' wrapper function,
        # so we have to manually hit the worklog/list endpoint ourselves
        resp: Response = retry_for_status(
            jira_connection._session.post,
            url=jira_connection._get_url("worklog/list"),
            data=json.dumps({"ids": updated_worklog_ids}),
        )
        try:
            worklog_list_json = resp.json()
        except ValueError:
            logger.error(f"Couldn't parse JIRA response as JSON: {resp.text}")
            raise

        updated.extend([wl for wl in worklog_list_json if int(wl["issueId"]) in issue_ids])
        if worklog_ids_json["lastPage"]:
            break
        updated_since = worklog_ids_json["until"]
    logger.info("Done fetching updated worklogs")

    logger.info("Fetching deleted worklogs")
    while True:
        try:
            worklog_ids_json = retry_for_status(
                jira_connection._get_json,
                "worklog/deleted",
                params={"since": deleted_since},
            )

            deleted_ids.extend([v["worklogId"] for v in worklog_ids_json["values"]])

            if worklog_ids_json["lastPage"]:
                break
            deleted_since = worklog_ids_json["until"]
        except Exception as e:
            # Getting deleted worklogs is wildly under performant, for some Jira Server instances.
            # Most people, however, don't seem to need deleted work logs at all. Agent, for example,
            # has never ingest deleted work logs since it's inception. I think it's pretty safe to
            # not ingest delete work logs if we encounter a connection error here (which typically means)
            #
            # Jira ticket to improve deleted worklogs via the API: https://jira.atlassian.com/browse/JRASERVER-66180
            # Note that the submitted has given up on them fixing it, and posted work arounds for how to
            # ingest this data directly
            #
            logging_helper.send_to_agent_log_file(
                f'Error encountered when fetching deleted worklogs. Error message: {e}.',
                level=logging.ERROR,
                exc_info=True,
            )
            logging_helper.send_to_agent_log_file(
                f'This error WILL NOT be raised', level=logging.ERROR
            )
            break
    logger.info("Done fetching deleted worklogs")

    logger.info(
        f"Done downloading Worklogs! Found {len(updated)} worklogs and {len(deleted_ids)} deleted worklogs"
    )

    return {"existing": updated, "deleted": deleted_ids}


@jelly_trace
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_statuses(jira_connection: JIRA) -> list[dict]:
    """Fetches a list of Jira Statuses returned from the Jira status API endpoint

    Args:
        jira_connection (JIRA): A Jira connection, through their jira Python module

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains a 'status_id' key and a 'raw_json' field
    """
    logger.info("Downloading Jira Statuses...")
    result = [
        {"status_id": status.id, "raw_json": status.raw}
        for status in retry_for_status(jira_connection.statuses)
    ]
    logger.info(f"Done downloading Jira Statuses! Found {len(result)}")
    return result


def has_read_permissions(jira_connection: JIRA, project: Project) -> bool:
    """Given a project we know of, can we actually access it
        Some projects we have local no longer exist on remote or we no longer have access to
        other projects even come back from the api request (JIRA.projects()) but appear to be inaccessible
    Args:
        jira_connection (JIRA): A JIRA connection object
        project (JIRA.project): A JIRA project object
    Returns:
        bool: True if we have access to the project, False if we do not
    """
    if hasattr(project, 'isPrivate'):
        return not project.isPrivate
    project_perms_response = retry_for_status(jira_connection.my_permissions, project)
    has_perms: bool = project_perms_response['permissions']['BROWSE']['havePermission']
    return has_perms
