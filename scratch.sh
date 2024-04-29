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
