# Skill: persistent-context

Persists session state to long-term memory at the end of every successful task.

## Trigger
Invoked by `agents/orchestrator.md` Step 4 (Terminal) on every successful completion. Also safe to invoke manually via the runtime when a session is being closed.

## Inputs
- `sessionId` (from `memory/session/state.json`)
- `tier` (ATOMIC | FEATURE | ARCHITECTURAL)
- `objective` (from clarifier output)
- `patchesApplied` (list of file paths touched during the run)
- `decisions` (list of `<APPROVE>` / `<REJECT>` outcomes and their rationale)

## Behavior
1. Append a session entry to `memory/project/sessions.log` (create if missing) with: timestamp, sessionId, tier, objective, patchesApplied, decisions, durationMs.
2. If any architectural decision was approved, mirror it into `memory/project/architecture.md` under a `## Recent Changes` heading (most recent first, cap at 10 entries).
3. If any new mistakes were appended by `reflection`, do nothing further — `mistakes.md` is already authoritative.
4. Compact `memory/session/state.json` back to its initial shape (preserving `sessionId`) so the next task starts clean. Reset all retry counters to 0.

## Output
A single line: `persistent-context: ok (<N> sessions logged)`.
