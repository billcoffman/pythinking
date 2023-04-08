import requests

# Replace these with your values
base_url = 'https://github.x.com/api/v3'  # Replace with your GitHub Enterprise base API URL
owner = 'your-repo-owner'
repo = 'your-repo-name'
token = 'your-personal-access-token'

# Fetch default branch
url = f'{base_url}/repos/{owner}/{repo}'
headers = {'Authorization': f'token {token}'}
response = requests.get(url, headers=headers)
response.raise_for_status()
default_branch = response.json()['default_branch']

# Fetch all branches
url = f'{base_url}/repos/{owner}/{repo}/branches'
params = {'per_page': 100}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
branches = response.json()

# Find merged branches
merged_branches = []
for branch in branches:
    branch_name = branch['name']
    if branch_name == default_branch:
        continue

    url = f'{base_url}/repos/{owner}/{repo}/branches/{branch_name}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.json().get('merged'):
        merged_branches.append(branch_name)

print("Merged branches:")
for branch in merged_branches:
    print(branch)
