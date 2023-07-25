import requests
from datetime import datetime, timezone

def parse_iso8601(date_string):
    """Parses an ISO 8601 date string to a datetime object"""
    return datetime.strptime(date_string.rstrip('Z'), '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc)

def get_run_times(token, owner, repo, pr_number):
    # Setup headers for requests
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept': 'application/vnd.github.v3+json'
    }

    # URL for the checks associated with the given PR
    checks_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/check-runs'

    # Send request
    response = requests.get(checks_url, headers=headers)
    response.raise_for_status()

    # Get the JSON data from the response
    data = response.json()

    # Check if there are any check runs
    if not data.get('check_runs'):
        print('No check runs found for this PR.')
        return

    # Initialize min start time and max end time
    min_start_time = None
    max_end_time = None

    # Iterate over all check runs
    for check_run in data['check_runs']:
        start_time = parse_iso8601(check_run['started_at'])
        end_time = parse_iso8601(check_run['completed_at'])
        status = check_run['status']

        # Check if this start time is the earliest
        if min_start_time is None or start_time < min_start_time:
            min_start_time = start_time

        # Check if this end time is the latest
        if max_end_time is None or end_time > max_end_time:
            max_end_time = end_time

        # Print check run details
        elapsed_time = end_time - start_time
        print(f'Check run: {check_run["name"]}, Elapsed time: {elapsed_time}, Status: {status}')

    # Print total time
    total_time = max_end_time - min_start_time
    print(f'Total time for all check runs: {total_time}')

if __name__ == '__main__':
    YOUR_GITHUB_TOKEN = 'your_token_here'
    OWNER = 'owner'
    REPO = 'repo'
    PR_NUMBER = 123

    get_run_times(YOUR_GITHUB_TOKEN, OWNER, REPO, PR_NUMBER)
