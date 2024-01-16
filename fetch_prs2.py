from python_graphql_client import GraphqlClient
import os
import sys

client = GraphqlClient(endpoint="https://api.github.com/graphql")
token = os.getenv('GH_TOKEN')
auth = {"Authorization": f"Bearer {token}"}

commit_schema = """
  pageInfo {
    endCursor
    hasNextPage
  }
  nodes {
    commit {
      oid
    }
  }
"""

review_schema = """
  pageInfo {
    endCursor
    hasNextPage
  }
  nodes {
    author {
      login
    }
    state
    createdAt
  }
"""

pr_query = """
query($repoName: String!, $owner: String!, $afterCursor: String) {
  repository(name: $repoName, owner: $owner) {
    pullRequests(first: 10, after: $afterCursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        number
        title
        commits(first: 100) {
          ${commit_schema}
        }
        reviews(first: 100) {
          ${review_schema}
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
        ${commit_schema}
      }
    }
  }
}
"""

review_query = """
query($repoName: String!, $owner: String!, $prNumber: Int!, $afterCursor: String) {
  repository(name: $repoName, owner: $owner) {
    pullRequest(number: $prNumber) {
      reviews(first: 100, after: $afterCursor) {
        ${review_schema}
      }
    }
  }
}
"""


def fetch_more_commits(repo_name, owner, pr_number, after_cursor):
    while True:
        variables = {
            "repoName": repo_name,
            "owner": owner,
            "prNumber": pr_number,
            "afterCursor": after_cursor
        }
        data = client.execute(query=commit_query, variables=variables,
                              headers=auth)
        commits_data = data["data"]["repository"]["pullRequest"]["commits"]
        for commit in commits_data["nodes"]:
            yield commit["commit"]
        if not commits_data["pageInfo"]["hasNextPage"]:
            break
        after_cursor = commits_data["pageInfo"]["endCursor"]


def fetch_prs(repo_name, owner):
    has_next_page = True
    after_cursor = None
    commit_queue = []
    hdr = auth
    while has_next_page:
        variables = {
            "repoName": repo_name,
            "owner": owner,
            "afterCursor": after_cursor
        }
        data = api.gq(query=pr_query, variables=variables, headers=hdr)
        prs_data = data["data"]["repository"]["pullRequests"]
        for pr in prs_data["nodes"]:
            print(f"PR {pr['number']} - {pr['title']}")
            for commit in pr["commits"]["nodes"]:
                print(f" - Commit: {commit['commit']['oid']}")
        if pr["commits"]["pageInfo"]["hasNextPage"]:
            # Save PR number and endCursor for additional commits
            commit = (pr['number'], pr["commits"]["pageInfo"]["endCursor"])
            commit_queue.append(commit)

    # Process the next commits queue
    for pr_num, cursor in commit_queue:
        for commit in fetch_additional_commits(repo_name, owner,
                                               pr_number, end_cursor):
            print(f" - Additional Commit: {commit['oid']}")

    has_next_page = prs_data["pageInfo"]["hasNextPage"]
    after_cursor = prs_data["pageInfo"]["endCursor"]

    # Clear the next commits queue after processing
    next_commits_queue.clear()


def get_commit(repo_name, owner, pr_number):
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
                              headers=auth)
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
                              headers=auth)
        prs = data["data"]["repository"]["pullRequests"]
        for pr in prs["nodes"]:
            print(f"PR {pr['number']} - {pr['title']}")
            for commit in get_commit(repo_name, owner, pr['number']):
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

