def get_all_comments_for_all_prs(api, owner, repo_name):
    all_comments = []
    for pr in api.get_pull_requests(owner, repo_name):
        pr_number = pr["number"]
        comments = api.get_pull_request_comments(owner, repo_name, pr_number)
        all_comments.extend(comments)
    return all_comments

# Usage example:
owner = 'your-repo-owner'
repo_name = 'your-repo-name'
all_comments = get_all_comments_for_all_prs(api, owner, repo_name)

print("Total comments:", len(all_comments))
