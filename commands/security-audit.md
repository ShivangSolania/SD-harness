# Command: /security-audit
Triggers an immediate end-to-end vulnerability evaluation of the active workspace.

## Execution Sequence
1. Invoke `agents/security.md` across all files modified within the current branch or commit delta.
2. Cross-reference project dependencies against known vulnerability databases using fast, non-interactive terminal check tools.