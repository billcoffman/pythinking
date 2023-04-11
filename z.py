import requests
import unittest
from unittest.mock import patch

class GitHubAPI:
    # ... (previous code)

    def get_pull_request_comments(self, owner, repo_name, pr_number):
        """
        Fetches comments for a pull request.

        :param owner: str, Repository owner's username
        :param repo_name: str, Repository name
        :param pr_number: int, Pull request number
        :return: list of dicts, Pull request comments
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.base_url}/repos/{owner}/{repo_name}/pulls/{pr_number}/comments'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

# Mock data for testing
mock_valid_comments = [
    {
        "id": 1,
        "user": {
            "login": "user1"
        },
        "body": "Comment 1"
    },
    {
        "id": 2,
        "user": {
            "login": "user2"
        },
        "body": "Comment 2"
    }
]

# Unit tests structure
class TestGitHubAPI(unittest.TestCase):
    # ... (previous code)

    @patch('requests.get')
    def test_get_pull_request_comments_valid(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_valid_comments

        owner = 'your-repo-owner'
        repo_name = 'your-repo-name'
        pr_number = 1
        comments = self.api.get_pull_request_comments(owner, repo_name, pr_number)

        assert comments is not None
        assert isinstance(comments, list)
        assert len(comments) == 2

    @patch('requests.get')
    def test_get_pull_request_comments_invalid(self, mock_get):
        mock_get.return_value.status_code = 404

        owner = 'your-repo-owner'
        repo_name = 'your-repo-name'
        pr_number = 9999

        with self.assertRaises(requests.exceptions.HTTPError):
            self.api.get_pull_request_comments(owner, repo_name, pr_number)

if __name__ == '__main__':
    unittest.main()

