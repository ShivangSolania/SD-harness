# Skill: compact

Summarizes and prunes the active context window when it approaches capacity.

## Trigger
Invoked by `agents/orchestrator.md` Step 4 (Terminal) — but ONLY when either threshold in `harness.jsonc.compactThreshold` is crossed:
- `contextPct` > 50 (context window utilization), OR
- `toolOutputs` > 5 (cumulative tool output turns in this session)

## Inputs
- The current session transcript (messages + tool outputs).
- `memory/session/state.json` for tier + objective.

## Behavior
1. Identify tool outputs older than the last `coder`/`reviewer` exchange that are unlikely to be referenced again (heuristics: long stdout, full-file dumps, completed test runs). Replace each with a 1-3 line summary.
2. Summarize the `researcher` and `hermes-reasoner` outputs into a single `## Compressed Context` block at the top of the working context.
3. Preserve verbatim:
   - The original user objective.
   - The clarifier tier tag.
   - The current `memory/session/state.json` snapshot.
   - The most recent `<surgical_patch>` block (in case a retry needs it).
4. Write the discarded raw context to `context/compression/<sessionId>-<timestamp>.jsonl` so nothing is lost.

## Output
A single line: `compact: ok (kept <X> tokens, archived <Y> tokens)`.
