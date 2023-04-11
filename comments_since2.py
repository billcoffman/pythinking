import requests

class GitHubAPI:
    # ... (previous code)

    def get_all_pull_request_comments_since(self, owner, repo_name, since=None):
        """
        Fetches all pull request review comments for a repository, updated after a specific date.

        :param owner: str, Repository owner's username
        :param repo_name: str, Repository name
        :param since: str, ISO 8601 timestamp to fetch comments updated after this time. Defaults to None
        :return: list of dicts, Pull request review comments
        :raises: requests.exceptions.HTTPError if API call fails
        """
        url = f'{self.base_url}/repos/{owner}/{repo_name}/pulls/comments'
        params = {
            'sort': 'updated',
            'direction': 'desc',  # Ensure we get the most recently updated comments first
            'page': 1,
            'per_page': 100  # Adjust as needed, maximum is 100
        }

        all_comments = []
        has_more_comments = True

        while has_more_comments:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            comments = response.json()

            if not comments:
                break

            for comment in comments:
                updated_at = comment['updated_at']
                if since is not None and updated_at <= since:
                    has_more_comments = False
                    break
                all_comments.append(comment)

            params['page'] += 1

        return all_comments

# Usage example:
owner = 'your-repo-owner'
repo_name = 'your-repo-name'
last_updated_timestamp = '2023-01-01T00:00:00Z'
comments_since_last_update = api.get_all_pull_request_comments_since(owner, repo_name, since=last_updated_timestamp)

