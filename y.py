import requests
import unittest
from unittest.mock import patch

class GitHubAPI:
    def __init__(self, token, base_url='https://github.x.com/api/v3'):
        """
        Constructor for the GitHubAPI class.

        :param token: str, Personal Access Token for authentication
        :param base_url: str, Base URL for the GitHub API. Defaults to GitHub Enterprise base API URL
        """
        self.token = token
        self.base_url = base_url
        self.headers = {'Authorization': f'token {self.token}'}

    def get_repo(self, owner, repo_name):
        """
        Fetches information about a repository.

        :param owner: str, Repository owner's username
        :param repo_name: str, Repository name
        :return: dict, Repository information
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.base_url}/repos/{owner}/{repo_name}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


# Mock data for testing
mock_valid_repo = {
    "name": "your-repo-name",
    "owner": {
        "login": "your-repo-owner"
    }
}

# Unit tests structure
class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        token = 'your-personal-access-token'
        self.api = GitHubAPI(token)

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

