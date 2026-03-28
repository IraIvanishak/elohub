#!/bin/bash
# scripts/claude-pr-prep.sh
# Generate a PR description from the current branch's changes vs main

set -e

BRANCH=$(git branch --show-current)
BASE=${1:-main}

if [ "$BRANCH" = "$BASE" ]; then
  echo "Error: already on $BASE — switch to a feature branch first"
  exit 1
fi

echo "Preparing PR description for '$BRANCH' against '$BASE'..."

DIFF=$(git diff "$BASE"..."$BRANCH" --stat)

if [ -z "$DIFF" ]; then
  echo "No changes found between $BASE and $BRANCH"
  exit 0
fi

PR_DESC=$(claude -p "Generate a GitHub PR description for branch '$BRANCH'.

Here are the changed files:
$DIFF

Read the changed files and produce:
- A short PR title (under 70 chars)
- A summary section with 2-3 bullet points
- A test plan checklist

Format as markdown." --max-turns 5 --allowedTools Read,Glob,Grep)

echo ""
echo "===== Suggested PR Description ====="
echo "$PR_DESC"
