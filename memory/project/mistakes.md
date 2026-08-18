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

### 2026-08-18 — hallucinated-symbol-in-patch
- **Symptom:** Coder emitted an Express middleware reference that does not exist in package.json; reviewer passed it.
- **Root cause:** Reviewer was not checking symbol existence, only style and type correctness.
- **Negative constraint:** Do NOT emit `PASS` when a new import or middleware identifier in `<new_replace>` cannot be confirmed in `package.json`, stdlib, or an existing local module.

### 2026-08-18 — researcher-context-overflow
- **Symptom:** Researcher output saturated 50% of the context window on the ARCHITECTURAL run, triggering a premature `compact` and burning the researcher's retry budget.
- **Root cause:** No output cap on researcher sections; wide-scope architectural queries produce unbounded output.
- **Negative constraint:** Do NOT emit more than 20 entries per section in researcher output. Truncate and note `> N more items omitted`.

