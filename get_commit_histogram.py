import requests
from collections import defaultdict
from datetime import datetime

# Replace these with your values
base_url = 'https://api.github.com'  # Use your GitHub Enterprise base API URL if applicable
owner = 'your-repo-owner'
repo = 'your-repo-name'
branch = 'your-branch-name'
token = 'your-personal-access-token'

headers = {'Authorization': f'token {token}'}
params = {'sha': branch, 'per_page': 100}

# Fetch commits
url = f'{base_url}/repos/{owner}/{repo}/commits'
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
commits = response.json()

# Create histogram of commits by date
histogram = defaultdict(int)
for commit in commits:
    commit_date_str = commit['commit']['committer']['date']
    commit_date = datetime.fromisoformat(commit_date_str).date()
    histogram[commit_date] += 1

print("Histogram of commits:")
for date, count in sorted(histogram.items()):
    print(f"{date}: {count}")
