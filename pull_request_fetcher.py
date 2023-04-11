import os

import requests

"""
We get 4 streams and join them.
1. PRs
   - open PRs counted if current, last commit to source branch < 60 days
   - PRs, open, closed, or old, will only be used if there are current reviewer comments
2. comments on PRs
   - comments on PRs tell us if reviewers are active.
3. branches
   - closed branches:
     * closed branches not included in feature branch stats
   - open branches
     * old branch: last commit was over 60 days ago
       - not considered for branch stats
     * current/open branch with closed PR
       - closed PR indicates the intent that the PR was created in error - ignore.
     * obsolete/current branch with merged PR
       - merged PR means this branch should be closed, it was an oversight not to close
       - possibly include in process violation (WoW)
       - WoW says branch should not have commits after the merge, but if ...
         * if the branch has commits after the PR was merged,
           it should be considered equivalent to a new branch without a PR.
           The commits will age out, or the branch will be closed to resolve this.
     * closed branch with merged PR:
       included with merged PR stats
   - default branches not included in branch stats
4. PRs on branches
   - closed branches with closed PR, used for reviewer stats if reviews current
5. commits on branches
   - obsolete/old branch: last commit was over 60 days ago
     * if old branch is part of current PR, again,
       it will be considered for reviewer stats if current
"""

GITHUB_IP_ADDR = 'gh.asml.com'
GITHUB_OWNER = 'asml-gh'
GITHUB_TOKEN = os.environ['GITHUB_PR_FETCHER_APP_TOKEN']


class PullRequestFetcher:
    """
    Core of GitHub_PR_Fetcher app.
    """
    def __init__(self, repo, token=None, owner=None, base_url=None):
        """
        Constructor for the GitHubAPI class.

        :param token: str, Personal Access Token for authentication
        :param base_url: str, Base URL for the GitHub API. Defaults to GitHub Enterprise base API URL
        """
        self.repo = repo  # Required, as in github.com/owner/repo.git
        self.base_url = base_url or f'https://{GITHUB_IP_ADDR}/api/v3'
        self.owner = owner or GITHUB_OWNER
        self.token = token or GITHUB_TOKEN
        self.per_page = 100
        self.headers = {'Authorization': f'token {self.token}'}
        self.repo_url = f'{self.base_url}/repos/{self.owner}/{self.repo}'

    def reset_repo(self, new_repo_name):
        """ Reset repo name reset state vars to init. """

        self.repo = new_repo_name
        self.repo_url = f'{self.base_url}/repos/{self.owner}/{self.repo}'

    def get_repo_info(self):
        """
        Fetches information about a repository.

        :return: dict, Repository information
        :raises: requests.exceptions.HTTPError if API call fails
        """
        response = requests.get(self.repo_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def pull_request_iterator(self):
        """
        Generator to iterate through the pull_request objects.
        :return: None
        """
        # since:date, sha:branch
        params = {'state': 'all', 'per_page': self.per_page}
        url = f'{self.repo_url}/pulls'
        while url:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            pr_list = response.json()
            for pr in pr_list:
                yield pr

            # Pagination: get the next URL from the Link header
            link_header = response.headers.get('Link')
            if link_header:
                links = [link.strip() for link in link_header.split(',')]
                urls = [link for link in links if 'rel="next"' in link]
                if not urls:
                    return
                url = urls[0][urls[0].find("<") + 1:urls[0].find(">")]

    @staticmethod
    def get_pull_request_status(pr):
        if pr["state"] == "open":
            return "open"
        elif pr["state"] == "closed" and pr["merged_at"] is not None:
            return "merged"
        elif pr["state"] == "closed" and pr["merged_at"] is None:
            return "closed"
        else:
            return "unknown"

    def get_pull_request_comments(self, pr_number):
        """
        Fetches comments for a pull request.

        :param pr_number: int, Pull request number
        :return: list of dicts, Pull request comments
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.repo_url}/pulls/{pr_number}/comments'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
