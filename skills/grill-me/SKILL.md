# Skill: grill-me

An adversarial interview skill that probes an architectural change request before it reaches the `architect` agent.

## Trigger
Invoked by `agents/orchestrator.md` Step 3 (`<ARCHITECTURAL>` tier), before `architect`.

## Inputs
- The user's original architectural change request.
- The current `memory/project/architecture.md` map.

## Behavior
1. Generate exactly 3 high-signal questions, one per dimension:
   - **Cost**: What is the migration / runtime / cognitive cost of this change? Name a concrete number or scope.
   - **Reversibility**: If we ship this and we're wrong, what is the rollback path? Is it days, weeks, or irreversible?
   - **Alternatives**: Name at least one cheaper alternative the user has rejected, and why.
2. Present the 3 questions to the user and wait for answers.
3. Once all 3 are answered, package the answers as an "interview transcript" and forward to `architect` as input. Do NOT make the approve/reject decision yourself.

## Output Format

```
## Grill-Me Interview
Q1 (Cost): <question>
A1: <user answer>

Q2 (Reversibility): <question>
A2: <user answer>

Q3 (Alternatives): <question>
A3: <user answer>
```

## Hard Limits
- Maximum 1 round of questions. Do not loop. If the user's answers are still ambiguous, forward the transcript anyway and let `architect` decide `<APPROVE>` or `<REJECT>`.
- Never ask more than 3 questions. Quality over quantity.
