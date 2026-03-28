---
name: test-flows
description: Analyze recent changes and recommend test flows to verify them
---

# Instructions

1. Run `git diff` to see unstaged changes, and `git diff --cached` for staged changes
2. If no uncommitted changes, run `git log -1 --stat` to check the most recent commit
3. For each changed file, identify which area of the app is affected:
   - `app/routes/` — determine which blueprint and endpoints changed
   - `app/services/` — identify which business logic changed and what routes call it
   - `app/platforms/` — identify which platform adapter changed and what profiles use it
   - `app/models.py` — flag any schema changes that affect multiple areas
   - `app/templates/` — note which pages need visual verification
   - `seed.py` or `run.py` — flag startup/initialization changes

4. For each affected area, output a concrete test flow the developer should walk through manually

# Output Format

## Changed Files
[List the files that changed with a one-line summary of each change]

## Recommended Test Flows

For each flow, provide:
- **Flow name**: Short description
- **Steps**: Numbered walkthrough (e.g., "1. Start the server, 2. Go to /profile, 3. Connect Chess.com account, 4. Verify scores display")
- **What to verify**: Specific things to check (correct data, no errors, UI renders properly)
- **Risk level**: Low / Medium / High — based on how many other parts of the app the change touches

## Quick Smoke Test
[Always include a minimal smoke test: start the server, log in, visit the main pages, verify no 500 errors]
