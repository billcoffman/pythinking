import requests

class GitHubAPI:
    # ... (previous code)

    def get_all_pull_request_comments_since(self, owner, repo_name, since=None):
        all_comments = []
        page = 1
        per_page = 100
        done = False

        while not done:
            url = f'{self.base_url}/repos/{owner}/{repo_name}/pulls/comments'
            params = {
                'sort': 'updated',
                'direction': 'desc',
                'page': page,
                'per_page': per_page
            }
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            comments = response.json()
            if not comments:
                break

            for comment in comments:
                if since and comment["updated_at"] <= since:
                    done = True
                    break
                all_comments.append(comment)

            page += 1

        return all_comments

# Usage example:
owner = 'your-repo-owner'
repo_name = 'your-repo-name'
last_updated_timestamp = '2023-01-01T00:00:00Z'
comments_since_last_update = api.get_all_pull_request_comments_since(owner, repo_name, since=last_updated_timestamp)

