name: Clone Repository Metadata

on:
  workflow_dispatch:

jobs:
  clone-metadata:
    runs-on: ubuntu-latest
    steps:
      - name: Clone repository metadata only
        run: git clone --no-checkout https://${{ secrets.GITHUB_TOKEN }}@gh.foo.com/owner/my-repo

#!/bin/bash

# Parameters
DIR="$1"
REPO_URL="$2"
BRANCH_NAME="$3"

# Environment variable check
if [[ -z "$GH_TOKEN" ]] || [[ ${#GH_TOKEN} -lt 10 ]]; then
  echo "GH_TOKEN is not set or is too short."
  exit 1
fi

# Change directory
cd "$DIR" || { echo "Failed to change directory to $DIR"; exit 1; }

# Check for .git directory
if [ -d ".git" ]; then
  NEED_CLONE=false
else
  NEED_CLONE=true
fi

# Clone repository if needed
if $NEED_CLONE; then
  echo "Cloning repository..."
  git clone --no-checkout "$REPO_URL" || { echo "Failed to clone repository."; exit 1; }
  cd "$(basename "$REPO_URL" .git)" || { echo "Failed to change directory to repository."; exit 1; }
fi

# Fetch all branches
git fetch --all

# Check for specific branch and get the first five commits
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  # Getting the first five commits, including branch creation
  COMMIT_INFO=$(git log "$BRANCH_NAME" --format="%H %ci" -5)
  if [ -z "$COMMIT_INFO" ]; then
    echo "No commits found on branch $BRANCH_NAME."
    exit 1
  fi
  # Output branch name and the date of the first commit (branch creation date)
  FIRST_COMMIT_DATE=$(echo "$COMMIT_INFO" | tail -1 | awk '{print $2}')
  echo "$BRANCH_NAME $FIRST_COMMIT_DATE"
else
  echo "Branch $BRANCH_NAME does not exist."
  exit 1
fi


git log --pretty=format:"%h %ad | %s [%an]" --date=short | while read line; do
    commit_hash=`echo $line | awk '{print $1}'`
    branches=$(git branch --contains $commit_hash | sed 's/^\* //g' | tr '\n' ' ')
    echo "$line | $branches"
done



#!/bin/bash
branch_name="your-branch"
r=1.5
commits=() # Initialize an empty array
index=0
pos1=0
pos2=0

# Function to determine if a commit hash is associated with multiple branches
multiple_branches() {
    local commit_hash=$1
    count=$(git branch -r --contains "$commit_hash" | wc -l)
    [ "$count" -gt 1 ]
}

# Function to fetch a single commit hash at a specific index
get_hash() {
    local idx=$1
    git log --first-parent --format="%H" $branch_name | sed "${idx}q;d"
}

# Start by fetching the first commit
h=$(get_hash 1)
commits[index]=$h

while true; do
    if [ $index -ge $pos2 ]; then
        if multiple_branches "${commits[$index]}"; then
            pos2=$index
        else
            pos1=$index
            pos2=$(awk "BEGIN{print int(($pos2 + 1) * $r)}")  # Calculate new pos2
        fi
    fi

    # Increment index and fetch next commit
    index=$((index + 1))
    h=$(get_hash $index)
    commits[index]=$h

    # Break if pos1 and pos2 converge
    if [ $((pos2 - pos1)) -le 1 ]; then
        echo "Transition at commit: ${commits[$pos1]}"
        break
    fi
done





#!/bin/bash

# Get the list of commits
commits=($(git log --first-parent --format="%H" branch-name))

# Initialize positions
pos1=0
pos2=${#commits[@]}-1

# Bisection search
while [ $((pos2 - pos1)) -gt 1 ]; do
    mid=$(((pos1 + pos2) / 2))
    mid_commit=${commits[$mid]}
    count=$(git branch -r --contains $mid_commit | wc -l)

    if [ "$count" -gt 1 ]; then
        pos1=$mid
    else
        pos2=$mid
    fi
done

# Output the commit where branches transition from many to one
echo "Transition at commit: ${commits[$pos2]}"



import subprocess
import sys

def run_bash_script(script_path):
    # Initialize variables to capture output and errors
    output = []
    errors = []

    # Start the subprocess
    with subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        while True:
            # Read stdout line by line
            out_line = proc.stdout.readline()
            if out_line:
                sys.stdout.write(out_line)  # Print to terminal
                output.append(out_line)  # Append to output list
            # Read stderr line by line
            err_line = proc.stderr.readline()
            if err_line:
                sys.stderr.write(err_line)  # Print to terminal
                errors.append(err_line)  # Append to error list

            # Break out of the loop if the process is done and there are no more lines to read
            if not out_line and not err_line and proc.poll() is not None:
                break

        # Optionally handle the case where there might still be data in the buffers
        stdout_remaining, stderr_remaining = proc.communicate()
        if stdout_remaining:
            sys.stdout.write(stdout_remaining)
            output.append(stdout_remaining)
        if stderr_remaining:
            sys.stderr.write(stderr_remaining)
            errors.append(stderr_remaining)

    # Convert lists of output and errors to single strings
    output_str = ''.join(output)
    errors_str = ''.join(errors)
    
    return output_str, errors_str

# Usage
script_path = 'your_script.sh'  # Path to your Bash script
output, errors = run_bash_script(script_path)
print("Captured Output:")
print(output)
print("Captured Errors:")
print(errors)



git log $HASH -1 --pretty=format:"%ad %H [%an] [%s]" --date=format:"%Y-%m-%dT%H:%M:%S" > line.txt


def parse_git_log():
    with open("line.txt") as line_file:
        line = line_file.readline()  # Read the single line of output
        date, hash, bracketed = line.split(" ", 2)  # Split into three parts
        bracketed = bracketed.strip()  # Strip any leading/trailing whitespace
        bracketed = bracketed.lstrip("[")  # Remove the first bracket
        bracketed = bracketed.rstrip("]")  # Remove the last bracket
        username, comment = bracketed.split("] [")  # Split the username and comment
        return date, hash, username, comment

# Example usage
date, hash, username, comment = parse_git_log()
print(f"Date: {date}, Hash: {hash}, Username: {username}, Comment: {comment}")



# Get the linear history of the branch
commits=$(git log --first-parent --format="%H" BRANCH)

# Assuming we have a way to check branch associations efficiently
previous_associations=()
for commit in $commits; do
  # Fetch branches associated with this commit
  current_associations=$(efficient_branch_association_check $commit)
  
  # Compare current associations with previous
  if [ ${#current_associations[@]} -lt ${#previous_associations[@]} ]; then
    echo "Branch created at commit $commit"
    break
  fi

  previous_associations=("${current_associations[@]}")
done
