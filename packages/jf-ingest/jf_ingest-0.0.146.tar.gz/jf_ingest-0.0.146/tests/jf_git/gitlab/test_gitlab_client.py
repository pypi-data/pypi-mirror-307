from unittest.mock import patch
import pytest
import requests
import requests_mock
from requests_mock.exceptions import NoMockAddress

from jf_ingest.config import GitAuthConfig
from jf_ingest.constants import Constants
from jf_ingest.jf_git.clients.gitlab import GitlabClient
from jf_ingest.utils import RetryLimitExceeded

TEST_COMPANY_SLUG = 'A-Company'
TEST_BASE_URL = 'https://www.a-website.com'
TEST_TOKEN = 'A Spoofed Token'
TEST_ORG_LOGIN = '1'
TEST_FULL_PATH = 'test-full-path'
EXPECTED_AUTH_HEADER = {
    'Authorization': f'Bearer {TEST_TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': f'{Constants.JELLYFISH_USER_AGENT} ({requests.utils.default_user_agent()})',
}

def test_gitlab_client_constructor():
    auth_config = GitAuthConfig(
        company_slug=TEST_COMPANY_SLUG,
        base_url=TEST_BASE_URL,
        token=TEST_TOKEN,
        verify=False,
    )
    client = GitlabClient(auth_config)
    assert client.company_slug == auth_config.company_slug
    assert client.gql_base_url == f'{auth_config.base_url}/api/graphql'
    assert client.rest_api_url == auth_config.base_url
    assert client.session.headers['Authorization'] == f'Bearer {auth_config.token}'
    assert client.session.headers['Content-Type'] == 'application/json'

def test_gitlab_client_constructor_with_passed_in_session():
    spoofed_session = requests.Session()
    spoofed_header_key = 'Spoofed-Header'
    spoofed_header_value = 123
    spoofed_session.headers.update({
        spoofed_header_key: spoofed_header_value
    })
    auth_config = GitAuthConfig(
        company_slug='A-Company',
        base_url='www.company.net',
        token='A Spoofed Token',
        verify=False,
        session=spoofed_session
    )
    client = GitlabClient(auth_config)
    assert client.company_slug == auth_config.company_slug
    assert client.gql_base_url == f'{auth_config.base_url}/api/graphql'
    assert client.rest_api_url == auth_config.base_url
    assert client.session.headers[spoofed_header_key] == spoofed_header_value



@pytest.fixture()
def client():
    auth_config = GitAuthConfig(
        company_slug=TEST_COMPANY_SLUG,
        base_url=TEST_BASE_URL,
        token=TEST_TOKEN,
        verify=False,
    )
    return GitlabClient(auth_config)

def test_get_raw_gql_result_simple(client: GitlabClient, requests_mock: requests_mock.Mocker):
    # Test Data
    test_query_body = "test_query_body"
    # Mock classes/data
    session_mock_caller_data = {'query': test_query_body}
    session_mock_return_data = {'data': {'test_key': 'test_value'}}
    requests_mock.post(url=f'{TEST_BASE_URL}/api/graphql', json=session_mock_return_data, request_headers=EXPECTED_AUTH_HEADER)

    # call function
    returned_data = client.get_raw_result_gql(query_body=test_query_body)

    assert returned_data == session_mock_return_data
    assert requests_mock.last_request.json() == session_mock_caller_data

def test_get_organization_full_path(client: GitlabClient, requests_mock: requests_mock.Mocker):
    requests_mock.get(
        url=f'{TEST_BASE_URL}/api/v4/groups/{TEST_ORG_LOGIN}?with_projects=False', 
        json={'full_path': TEST_FULL_PATH}, 
        request_headers=EXPECTED_AUTH_HEADER
    )
    
    full_path_response = client.get_organization_full_path(login=TEST_ORG_LOGIN)
    
    assert full_path_response == TEST_FULL_PATH
    
def test_get_raw_gql_results_retries_on_429s(mocker, client: GitlabClient, requests_mock: requests_mock.Mocker):
    attempts = 10
    requests_mock.post(url=f'{TEST_BASE_URL}/api/graphql', request_headers=EXPECTED_AUTH_HEADER, status_code=429)
    with mocker.patch('time.sleep', return_value=None), pytest.raises(RetryLimitExceeded):
        client.get_raw_result_gql('', max_attempts=attempts)
        assert requests_mock.call_count == attempts

def test_get_raw_gql_result_verify_headers_present(client: GitlabClient, requests_mock: requests_mock.Mocker):
    # Test Data
    test_query_body = "test_query_body"
    # Mock classes/data
    session_mock_caller_data = {'query': test_query_body}
    session_mock_return_data = {'data': {'test_key': 'test_value'}}
    requests_mock.post(url=f'{TEST_BASE_URL}/api/graphql', json=session_mock_return_data, request_headers=EXPECTED_AUTH_HEADER)

    # call function
    returned_data = client.get_raw_result_gql(query_body=test_query_body)

    assert returned_data == session_mock_return_data
    assert requests_mock.last_request.json() == session_mock_caller_data
 
def test_get_raw_gql_result_verify_headers_not_present(client: GitlabClient, requests_mock: requests_mock.Mocker):
    requests_mock.post(url=f'{TEST_BASE_URL}/api/graphql', json={}, request_headers={'Authorization': "A BAD TOKEN"})
    with pytest.raises(NoMockAddress):
        client.get_raw_result_gql(query_body='')
        
def test_page_results_gql_no_next_page(client: GitlabClient, requests_mock: requests_mock.Mocker):
    path_to_page_results = 'data.pages'
    query = """
        {{
            pages(first: 2, cursor: %s) {{
                pageInfo {{ hasNextPage, endCursor }}
                id, name
            }}
        }}
    """
    json_payload = {
            'data': {
                'pages': {
                    'pageInfo': {
                        'hasNextPage': False,
                        'endCursor': '123'
                    },
                    'page': [
                        {
                            'id': 1,
                            'name': 'one'
                        },
                        {
                            'id': 2,
                            'name': 'two'
                        }
                    ]
                }
            }
        }
    requests_mock.post(
        url=f'{TEST_BASE_URL}/api/graphql', 
        request_headers=EXPECTED_AUTH_HEADER,
        json=json_payload,
    )
    results = []
    for result_page in client.page_results_gql(query_body=query, path_to_page_info=path_to_page_results):
        for item in result_page['data']['pages']['page']:
            results.append(item)
            
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[1]['id'] == 2
    
        