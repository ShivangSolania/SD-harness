# Command: /explain-architecture
Walks a new contributor through the current project's architecture map.

## Execution Sequence
1. Read `memory/project/architecture.md` (the canonical map). If missing, halt and instruct the user to run a session first so `documentation` can populate it.
2. Cross-reference with `knowledge/architecture/` for any decision records (ADRs).
3. Render the architecture as a tree:
   - System boundaries (services / processes)
   - Primary datastores + schemas
   - Inbound/outbound integrations
   - Cross-cutting concerns (auth, logging, observability)
4. For each top-level node, print: purpose, owner (if recorded), and the file paths of the entrypoint + tests.
5. End with a "Key decisions" section listing the 3 most recent entries from `memory/project/patterns.md` if any.

## Output Format
Markdown, no chat preamble. Suitable for piping into `documentation` to refresh the README.
