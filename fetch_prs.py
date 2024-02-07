import json

class API:
    # ... (other parts of the class) ...

    def fetch_all_prs_and_reviews(self):
        all_prs_data = []
        pr_cursor = None  # Start with no cursor for the first page of PRs
        pr_has_next_page = True  # Assume there is at least one page of PRs
        pr_count = 0
        review_count = 0

        # Fetch all PRs and their reviews
        while pr_has_next_page:
            pr_data = self.fetch_record(review_cursor=None, pr_cursor=pr_cursor)
            prs = pr_data['data']['repository']['pullRequests']['edges']
            
            for pr in prs:
                pr_count += 1
                pr_number = pr['node']['number']
                reviews_data = pr['node']['reviews']['edges']
                review_page_info = pr['node']['reviews']['pageInfo']
                review_cursor = review_page_info['endCursor']

                # Fetch additional reviews for the PR if they exist
                while review_page_info['hasNextPage']:
                    additional_reviews_data = self.fetch_record(review_cursor=review_cursor, pr_cursor=None)
                    additional_reviews = additional_reviews_data['data']['repository']['pullRequests']['edges'][0]['node']['reviews']['edges']
                    review_count += len(additional_reviews)
                    reviews_data.extend(additional_reviews)
                    review_page_info = additional_reviews_data['data']['repository']['pullRequests']['edges'][0]['node']['reviews']['pageInfo']
                    review_cursor = review_page_info['endCursor']  # Ready for next pass, or ignored if no next page.

                # Combine the PR with all its reviews
                pr['node']['reviews']['edges'] = reviews_data  # Replace with combined reviews data.
                # Here you can process the PR and its reviews, e.g., print or save them
                extract_pr_and_reviews(pr)  # Dump the combined PR and reviews data
            
            # If there are no more PRs to fetch, break the loop
            pr_page_info = pr_data['data']['repository']['pullRequests']['pageInfo']
            pr_cursor = pr_page_info['endCursor']  # Set cursor for the next page of PRs
            pr_has_next_page = pr_page_info['hasNextPage']

        return

pr_query = """
query($repoName: String!, $owner: String!, $afterCursor: String) {
  repository(name: $repoName, owner: $owner) {
    pullRequests(first: 100, after: $afterCursor, states: OPEN) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        number
        title
        commits(first: 100) {
          nodes {
            commit {
              oid
            }
          }
        }
      }
    }
  }
}
"""
commit_query = """
query($repoName: String!, $owner: String!, $prNumber: Int!, $afterCursor: String) {
  repository(name: $repoName, owner: $owner) {
    pullRequest(number: $prNumber) {
      commits(first: 100, after: $afterCursor) {
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          commit {
            oid
          }
        }
      }
    }
  }
}
"""

def fetch_commits(repo_name, owner, pr_number):
    has_next_page = True
    after_cursor = None
    while has_next_page:
        variables = {
            "repoName": repo_name,
            "owner": owner,
            "prNumber": pr_number,
            "afterCursor": after_cursor
        }

        data = client.execute(query=commit_query, variables=variables,
                              headers={"Authorization": f"Bearer {token}"})
        commits_data = data["data"]["repository"]["pullRequest"]["commits"]
        for commit in commits_data["nodes"]:
            yield commit["commit"]

        has_next_page = commits_data["pageInfo"]["hasNextPage"]
        after_cursor = commits_data["pageInfo"]["endCursor"]

def fetch_prs(repo_name, owner):
    has_next_page = True
    after_cursor = None

    while has_next_page:
        variables = {
            "repoName": repo_name,
            "owner": owner,
            "afterCursor": after_cursor
        }
        data = client.execute(query=pr_query, variables=variables,
                              headers={"Authorization": f"Bearer {token}"})
        prs = data["data"]["repository"]["pullRequests"]
        for pr in prs["nodes"]:
            print(f"PR {pr['number']} - {pr['title']}")
            for commit in fetch_commits(repo_name, owner, pr['number']):
                print(f" - Commit: {commit['oid']}")
        has_next_page = prs["pageInfo"]["hasNextPage"]
        after_cursor = prs["pageInfo"]["endCursor"]
# ----------------------------
if __name__ == "__main__":
    prog = sys.argv.pop(0)
    if len(sys.argv) < 2:
        print(f"Usage: {prog} <repo_name> <owner>")
        sys.exit(1)

    repo_name, owner = sys.argv
    fetch_prs(repo_name, owner)
