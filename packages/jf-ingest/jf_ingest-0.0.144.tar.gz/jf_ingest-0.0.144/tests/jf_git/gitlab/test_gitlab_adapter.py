import pytest
from jf_ingest.config import GitAuthConfig, GitConfig, GitProvider
from jf_ingest.jf_git.adapters import GitAdapter
from jf_ingest.jf_git.adapters.gitlab import GitlabAdapter
from jf_ingest.jf_git.clients.gitlab import GitlabClient

TEST_COMPANY_SLUG = 'a-company'
TEST_INSTANCE_SLUG = 'an-instance-slug'
TEST_INSTANCE_FILE_KEY = 'an-instance-file-key'
TEST_TOKEN = 'a-token'
TEST_BASE_URL = 'https://www.a-website.com'

TEST_GIT_AUTH_CONFIG = GitAuthConfig(
        company_slug=TEST_COMPANY_SLUG,
        base_url=TEST_BASE_URL,
        token=TEST_TOKEN,
        verify=False,
    )

GITLAB_GIT_CONFIG = GitConfig(
    company_slug=TEST_COMPANY_SLUG,
    instance_slug=TEST_INSTANCE_SLUG,
    instance_file_key=TEST_INSTANCE_FILE_KEY,
    git_provider=GitProvider.GITLAB,
    git_auth_config=TEST_GIT_AUTH_CONFIG
)

def _get_gitlab_adapter() -> GitlabAdapter:
    return GitAdapter.get_git_adapter(GITLAB_GIT_CONFIG)

def test_gitlab_adapter():
    gitlab_adapter = _get_gitlab_adapter()
    assert type(gitlab_adapter) == GitlabAdapter
    assert gitlab_adapter.config.git_provider == GitProvider.GITLAB
    assert type(gitlab_adapter.client) == GitlabClient
    
@pytest.fixture
def gitlab_adapter():
    return _get_gitlab_adapter()
    
def test_gitlab_adapter_supports_date_filtering(gitlab_adapter: GitlabAdapter):
    assert gitlab_adapter.git_provider_pr_endpoint_supports_date_filtering() == True
    
def test_gitlab_adapter_get_api_scopes(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_api_scopes()
        
def test_gitlab_adapter_get_organizations(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_organizations()
    
def test_gitlab_get_users(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_users(standardized_organization=None)
        
def test_gitlab_get_teams(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_teams(
            standardized_organization=None
        )
        
def test_gitlab_get_repos(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_repos(
            standardized_organization=None
        )
        
def test_gitlab_get_commits_for_default_branch(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_commits_for_default_branch(
            standardized_repo=None
        )
        
def test_gitlab_get_branches_for_repo(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_branches_for_repo(
            standardized_repo=None
        )
        
def test_gitlab_get_commits_for_branches(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_commits_for_branches(
            standardized_repo=None,
            branches=[]
        )
        
def test_gitlab_get_pr_metadata(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_pr_metadata(
            standardized_repo=None,
        )
        
def test_gitlab_get_prs(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_prs(
            standardized_repo=None,
        )
    