# OpenCode Harness

A deterministic multi-agent orchestration harness for surgical code edits. Built around a thin orchestrator that routes user requests through a tiered pipeline (ATOMIC / FEATURE / ARCHITECTURAL) with hard retry budgets and persistent memory.

## Install

```bash
# 1. Drop the harness at its default location
mkdir -p ~/.config
unzip harness.zip -d ~/.config/   # creates ~/.config/harness/

# 2. Copy the example config and edit if needed
cp ~/.config/harness/harness.example.jsonc ~/.config/harness/harness.jsonc

# 3. (optional) override the harness root via env
export HARNESS_HOME=~/.config/harness
```

## Filesystem layout

```
~/.config/harness/
├── AGENTS.md                      # root guardrails (immutable)
├── harness.jsonc                  # runtime config (gitignored)
├── harness.example.jsonc          # config template
├── .gitignore
├── agents/                        # persona files (12 agents)
├── commands/                      # slash commands (6)
├── skills/                        # skill definitions
│   ├── claude-memory/persistent-context/
│   ├── compact/
│   └── grill-me/
├── workflows/                     # YAML workflows consumed by commands
├── knowledge/                     # long-lived reference docs
│   ├── architecture/
│   ├── best-practices/
│   ├── frameworks/
│   ├── libraries/
│   └── patterns/
├── memory/
│   ├── project/                   # architecture map, mistakes log, patterns
│   ├── session/state.json         # retry budget tracker (per session)
│   └── graph/                     # entity/relation graph (JSON)
├── observability/
│   └── failures.json              # append-only failure trace
├── sandbox/
│   ├── experiments/.thought.md    # hermes-reasoner scratchpad
│   └── temporary/                 # preview server root
├── scripts/
│   └── validate_surgical_patch.py # coder output validator
├── context/                       # context-engine scratch dirs
│   ├── compression/
│   ├── ranking/
│   ├── repository-index/
│   ├── retrieval/
│   └── summaries/
├── checkpoints/                   # snapshot/rollback storage
│   ├── recovery/
│   ├── rollback/
│   └── snapshots/
└── evaluations/                   # golden datasets + benchmark runner
    ├── datasets/
    ├── benchmarks/
    ├── reports/
    ├── metrics.json
    └── metrics.schema.json
```

## Quick start

```bash
# Atomic fix (single-file, single patch)
"Fix the typo in README.md line 42."

# Feature (multi-step, planned)
"Add a /healthz endpoint returning version + uptime as JSON."

# Architectural (interview + architect gate)
"Swap the primary datastore from Postgres to MongoDB."
```

## Pipeline

```
User request
   │
   ▼
[orchestrator] ── reads mistakes.md + patterns.md + models.json
   │
   ▼
[clarifier] ── emits <HALT> | <ATOMIC> | <FEATURE> | <ARCHITECTURAL>
   │
   ├─ ATOMIC ─────► coder → reviewer → security → tester → documentation
   │
   ├─ FEATURE ───► researcher → hermes-reasoner → planner
   │                → (per checklist item: coder → reviewer → security → tester)
   │                → documentation
   │
   └─ ARCHITECTURAL ► grill-me → architect
                       ├─ <APPROVE> → FEATURE sequence
                       └─ <REJECT>  → stop, relay critique

   │
   ▼
[persistent-context] → updates memory + architecture map
[compact]            → only if context > 50% or >5 tool outputs
```

Every gate has a hard retry budget of 1 (see `agents/orchestrator.md` Step 3). Retry counters are persisted in `memory/session/state.json` so a runaway loop is impossible.

## Secrets hygiene

* The security agent scans every `<surgical_patch>` for secret-like strings (AWS keys, GitHub tokens, Google OAuth refresh tokens, Slack tokens, PEM blocks) and halts the loop on detection.
* To extend the scanner, append patterns to `knowledge/best-practices/secret-patterns.md`.

The orchestrator refuses to start a run if any agent in the pipeline is unmapped.

## Surgical patch validator

```bash
python3 ~/.config/harness/scripts/validate_surgical_patch.py \
    --input <agent_output.txt> \
    --project-root <your_project_dir>
```

Exit codes:

| Code | Meaning |
|------|---------|
| 0 | all patches valid |
| 1 | malformed XML or empty `<old_search>` |
| 2 | `<old_search>` not found in target file |
| 3 | `<old_search>` matches multiple locations (ambiguous) |
| 4 | secret-like string detected in `<new_replace>` |
| 5 | IO error reading target file |

## Evaluation

Golden datasets live in `evaluations/datasets/`:

* `atomic-001.json` — single-file fix
* `feature-001.json` — multi-step feature
* `architectural-001.json` — architectural change with grill-me interview

Target metrics (`evaluations/metrics.json`):
* `target_hit_rate`: 0.95
* `surgical_patch_accuracy`: 1.0
* `allowed_hallucination_index`: 0.0

## Precedence

When two instructions conflict, higher-priority wins:

1. `AGENTS.md`
2. `agents/*.md`
3. `commands/*.md`
4. `skills/**/SKILL.md`

## License

Proprietary. See `LICENSE` if present, otherwise all rights reserved.
