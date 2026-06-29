# Command: /create-pr
Generates a PR description from the current session context and diff.

## Execution Sequence
1. Collect `git diff main` and the session's task summary.
2. Generate a structured PR body: Summary, Changes, Testing, Notes.
3. Output the PR markdown for the user to copy or submit.