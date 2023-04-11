def get_pull_request_merger(pr):
    if pr["merged_by"] is not None:
        return pr["merged_by"]["login"]
    return None

# Usage example:
pr = api.get_pull_request(owner, repo_name, pr_number)
merger = get_pull_request_merger(pr)
if merger:
    print(f"Pull request merged by: {merger}")
else:
    print("Pull request not merged or merger information not available.")

