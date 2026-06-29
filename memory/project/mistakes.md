# Mistakes Log

> Negative constraints extracted by `agents/reflection.md` from `observability/failures.json`. The orchestrator reads this file at Step 0 of every run and applies all entries as hard constraints.

## Format

```markdown
### [ISO timestamp] — <failure mode label>
- **Symptom:** <one line>
- **Root cause:** <one to two lines>
- **Negative constraint:** Do NOT <action> when <condition>.
```

(append new entries below this line — most recent first)
