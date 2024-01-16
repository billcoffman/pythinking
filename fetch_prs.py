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
