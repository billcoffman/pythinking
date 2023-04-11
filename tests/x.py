import requests

import os


class PullRequestFetcher:
    def __init__(self, token, base_url='https://github.x.com/api/v3'):
        """
        Constructor for the GitHubAPI class.

        :param token: str, Personal Access Token for authentication
        :param base_url: str, Base URL for the GitHub API. Defaults to GitHub Enterprise base API URL
        """
        self.token = token
        self.base_url = base_url
        self.headers = {'Authorization': f'token {self.token}'}

    def get_repo(self, repo_name):
        """
        Fetches information about a repository.

        :param repo_name: str, Repository name
        :return: dict, Repository information
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.base_url}/repos/{owner}/{repo_name}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


# Unit tests structure
    def test_get_repo_valid(self, api):
        owner = 'your-repo-owner'
        repo_name = 'your-repo-name'
        repo = api.get_repo(owner, repo_name)

        assert repo is not None
        assert isinstance(repo, dict)
        assert repo['name'] == repo_name

    def test_get_repo_invalid(self, api):
        owner = 'your-repo-owner'
        repo_name = 'non-existent-repo'

        with pytest.raises(requests.exceptions.HTTPError):
            api.get_repo(owner, repo_name)

