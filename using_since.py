import requests
from datetime import datetime

class GitHubAPI:
    # ... (previous code)

    def get_pull_requests(self, owner, repo_name, state='all', since=None):
        """
        Fetches pull requests for a repository.

        :param owner: str, Repository owner's username
        :param repo_name: str, Repository name
        :param state: str, State of pull requests to fetch, either 'open', 'closed', or 'all'. Defaults to 'all'
        :param since: str, ISO 8601 timestamp to fetch pull requests updated after this time. Defaults to None
        :return: list of dicts, Pull requests
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.base_url}/repos/{owner}/{repo_name}/pulls'
        params = {'state': state}

        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
