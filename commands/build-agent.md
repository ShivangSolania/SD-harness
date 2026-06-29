# Command: /build-agent
Scaffolds a new agent persona file under `agents/` with the canonical structure.

## Execution Sequence
1. Collect: `name`, `purpose` (one sentence), `tier` (one of `pre-flight | classify | execute | gate | terminal`), and an optional `model` hint.
2. Generate `agents/<name>.md` from the template below.
3. Append a routing entry to `config/models.json` so the orchestrator can dispatch to the new agent. If `model` is omitted, inherit from the orchestrator's default.
4. Print the new file path and the updated `models.json` entry.

## Template

```markdown
# Persona: <Name>
<purpose>

## Rules
1. <input contract>
2. <processing rules>
3. <output contract>

## Output Format
<concrete format spec>
```
