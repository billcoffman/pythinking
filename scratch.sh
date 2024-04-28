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

