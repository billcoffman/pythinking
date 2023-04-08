import requests

# Replace these with your values
owner = 'your-repo-owner'
repo = 'your-repo-name'
token = 'your-personal-access-token'

# Fetch merged pull requests
url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
headers = {'Authorization': f'token {token}'}
params = {'state': 'closed', 'per_page': 100}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
pulls = response.json()

# Extract merged branches
merged_branches = set()
for pull in pulls:
    if pull.get('merged_at') is not None:
        branch_name = pull['head']['ref']
        merged_branches.add(branch_name)

print("Merged branches:")
for branch in merged_branches:
    print(branch)
