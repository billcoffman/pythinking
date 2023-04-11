import unittest
from unittest.mock import patch

from pull_request_fetcher import PullRequestFetcher

# Mock data for testing
mock_valid_repo = {
    "name": "your-repo-name",
    "owner": {
        "login": "your-repo-owner"
    }
}


class TestPullRequestFetcher(unittest.TestCase):
    def setUp(self):
        token = 'your-personal-access-token'
        self.api = PullRequestFetcher(token)

    @patch('requests.get')
    def test_get_repo_valid(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_valid_repo

        owner = 'your-repo-owner'
        repo_name = 'your-repo-name'
        repo = self.api.get_repo(owner, repo_name)

        assert repo is not None
        assert isinstance(repo, dict)
        assert repo['name'] == repo_name

    @patch('requests.get')
    def test_get_repo_invalid(self, mock_get):
        mock_get.return_value.status_code = 404

        owner = 'your-repo-owner'
        repo_name = 'non-existent-repo'

        with self.assertRaises(requests.exceptions.HTTPError):
            self.api.get_repo(owner, repo_name)


if __name__ == '__main__':
    unittest.main()

# Unit tests structure
class TestGitHubAPI(unittest.TestCase):

    def test_init(self):
        """
        Test the __init__ method of the GitHubAPI class.
        """

        @pytest.fixture
        def api(self):
            token = 'your-personal-access-token'
            return GitHubAPI(token)

    def test_get_repo(self, api):
        """
        Test the get_repo method of the GitHubAPI class.
        """
        owner = 'your-repo-owner'
        repo_name = 'your-repo-name'
        repo = api.get_repo(owner, repo_name)

        assert repo is not None
        assert isinstance(repo, dict)
        assert repo['name'] == repo_name

    def test_get_repo_neg(self, api):
        owner = 'your-repo-owner'
        repo_name = 'non-existent-repo'

        with pytest.raises(requests.exceptions.HTTPError):
            api.get_repo(owner, repo_name)

    def test_get_pull_requests(self):
        """
        Test the get_pull_requests method of the GitHubAPI class.
        """

    def test_get_pull_request_comments(self):
        """
        Test the get_pull_request_comments method of the GitHubAPI class.
        """

