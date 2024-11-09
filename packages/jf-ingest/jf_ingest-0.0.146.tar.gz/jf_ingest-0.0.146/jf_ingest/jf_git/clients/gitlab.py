import json
import logging
from typing import Dict, Generator

import requests

from jf_ingest.config import GitAuthConfig
from jf_ingest.constants import Constants
from jf_ingest.utils import retry_for_status, retry_session

logger = logging.getLogger(__name__)


class GitlabClient:

    def __init__(self, auth_config: GitAuthConfig, **kwargs):
        """Gitlab Client, used as a wrapper for getting raw data from the API.
        This client will get data mainly from the GraphQL API endpoints, although
        it will use the REST API endpoints for a small amount of functions as well.

        Args:
            auth_config (GitAuthConfig): A valid GitAuthConfiguration object
            kwargs: kwargs are used to pass arguments to the inner Session object, if no session object is provided as part of the GitAuthConfig
        """
        self.company_slug = auth_config.company_slug
        self.rest_api_url = auth_config.base_url
        self.gql_base_url = f'{auth_config.base_url}/api/graphql'
        if session := auth_config.session:
            self.session = session
        else:
            self.session = retry_session(**kwargs)
            self.session.headers.update(
                {
                    'Authorization': f'Bearer {auth_config.token}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'{Constants.JELLYFISH_USER_AGENT} ({requests.utils.default_user_agent()})',
                }
            )
        self.session.verify = auth_config.verify

    def get_organization_full_path(self, login: str) -> str:
        """In Jellyfish Land, the JFGithubOrganization is the normalization of Github Organizations,
        AzureDevops Organizations, Bitbucket Projects, and Gitlab Groups. The login field is the unique
        key. For Gitlab Groups, we set the login to the be the Group ID, which is a numeric value.
        The GraphQL Group Queries accept a "fullPath" argument, and NOT the Group ID. If we only have
        the GroupID (set by the login value), then this helper function can be used to translate the
        GroupID to a Full Path.
        NOTE: For performance reasons, we should probably graph the FullPath when we query GraphQL for
        Groups in general, and then cache those values. We should NOT call this function everytime,
        because it could have performance implications

        Args:
            login (str): The JFGithubOrganization login, which is the Group ID in Gitlab land
        """
        group_url = f'{self.rest_api_url}/api/v4/groups/{login}?with_projects=False'
        response: requests.Response = retry_for_status(self.session.get, url=group_url)
        response.raise_for_status()
        return str(response.json()['full_path'])

    def get_raw_result_gql(self, query_body: str, max_attempts: int = 7) -> Dict:
        """Gets the raw results from a Graphql Query.

        Args:
            query_body (str): A query body to hit GQL with
            max_attempts (int, optional): The number of retries we should make when we specifically run into GQL Rate limiting. This value is important if the GQL endpoint doesn't give us (or gives us a malformed) rate limit header. Defaults to 7.

        Raises:
            GqlRateLimitExceededException: A custom exception if we run into GQL rate limiting and we run out of attempts (based on max_attempts)
            Exception: Any other random exception we encounter, although the big rate limiting use cases are generally covered

        Returns:
            dict: A raw dictionary result from GQL
        """
        response: requests.Response = retry_for_status(
            self.session.post,
            url=self.gql_base_url,
            json={'query': query_body},
            max_retries_for_retry_for_status=max_attempts,
        )
        json_str = response.content.decode()
        json_data: Dict = json.loads(json_str)
        if error_list_dict := json_data.get('errors'):
            error_message = ','.join([error_dict.get('message') for error_dict in error_list_dict])
            raise Exception(f'An Error occurred when attempting to query GraphQL: {error_message}')

        return json_data

    def page_results_gql(
        self, query_body: str, path_to_page_info: str, cursor: str = 'null'
    ) -> Generator[Dict, None, None]:
        """This is a helper function for paging results from GraphQL. It expects
        a query body to hit Graphql with that has a %s marker after the "after:"
        key word, so that we can inject a cursor into the query. This will allow
        us to page results in GraphQL.
        To use this function properly, the section you are trying to page MUST
        INCLUDE VALID PAGE INFO (including the hasNext and endCursor attributes)

        Args:
            query_body (str): The query body to hit GraphQL with
            path_to_page_info (str): A string of period separated words that lead
            to the part of the query that we are trying to page. Example: data.organization.userQuery
            cursor (str, optional): LEAVE AS NULL - this argument is use recursively to page. The cursor
            will continuously go up, based on the endCursor attribute in the GQL call. Defaults to 'null'.

        Yields:
            Generator[dict, None, None]: This function yields each item from all the pages paged, item by item
        """
        hasNextPage = True
        while hasNextPage:
            # Fetch results
            result = self.get_raw_result_gql(query_body=(query_body % cursor))

            yield result

            # Get relevant data and yield it
            path_tokens = path_to_page_info.split('.')
            for token in path_tokens:
                result = result[token]

            page_info = result['pageInfo']
            # Need to grab the cursor and wrap it in quotes
            _cursor = page_info['endCursor']
            # If endCursor returns null (None), break out of loop
            hasNextPage = page_info['hasNextPage'] and _cursor
            cursor = f'"{_cursor}"'
