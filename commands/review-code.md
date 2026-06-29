# Command: /review-code
Triggers the code-review workflow on current uncommitted changes.

## Execution Sequence
1. Collect the current diff via `git diff`.
2. Execute `workflows/code-review.yaml` against the diff.
3. Output a combined verdict: quality + security + architecture.