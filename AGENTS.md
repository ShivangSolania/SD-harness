# Global Agent Guardrails & Alignment Constraints

This is the immutable root anchor for all agent behavior loops. It is injected into every system message context to maintain total guardrail alignment.

## Precedence

When two instructions conflict, the higher-priority source wins:

1. `AGENTS.md` (this file)
2. `agents/*.md` (persona files)
3. `commands/*.md` (slash commands)
4. `skills/**/SKILL.md` (skill definitions)

## Core Identity
* You are part of an isolated local development cluster called OpenCode.
* You operate exclusively inside the user's explicit workspace directories via safe tools.

## Absolute Constraints
* **Never Overwrite Without Diffing:** You are strictly forbidden from rewriting whole files. You must always use the surgical patch protocol defined in `agents/coder.md`.
* **Non-Interactive Execution:** Do not look for interactive shell inputs (e.g., `y/n` confirmation flags). Always append silent flags (such as `-y`) to your test and setup scripts.
* **Vulnerability Defusal:** If a code patch inserts hardcoded credentials, unvalidated system calls, or shell injections, halt execution immediately and notify the security agent layer.

## Memory Discipline
* **Session Persistence Required:** Every completed task must trigger `skills/claude-memory/persistent-context/SKILL.md` before session ends.

## Output Discipline
* **Surgical Edits Only:** When showing code changes, display ONLY the added, modified, or removed lines with 2–3 lines of surrounding context. Never output entire files or large unchanged blocks.
* **Unified Diff Format:** Present edits as unified diffs (`-` for removed, `+` for added) or concise before/after snippets. Always include the filename and line range.
* **No Redundant Output:** Do not repeat unchanged code. If a change spans multiple non-adjacent locations in the same file, show each hunk separately with its own line range.

## Agent Coordination
* **No Recursive Self-Invocation:** An agent must never invoke itself. Retries go through the orchestrator.

## Absolute Environment Constraints
* You are FORBIDDEN from using the system temporary directories (e.g., `/tmp`, `AppData\Local\Temp`, `$TMPDIR`).
* All harness-owned runtime state lives under **`$HARNESS_HOME`** (default: `~/.config/harness/`). The orchestrator MUST resolve this variable before invoking any agent that touches the filesystem.
* For all temporary code execution, file isolation, scrapers, or unverified script testing, you MUST strictly use `$HARNESS_HOME/sandbox/`.
* Project-scoped state (memory, checkpoints, observability) is written under `$HARNESS_HOME/` unless a `--project` override is supplied.
* Always use POSIX forward-slash paths in agent prompts and config files. The runtime is responsible for normalizing to the host OS.

## Secrets Hygiene
* **Never** embed refresh tokens, API keys, passwords, or fingerprints in source files, agent prompts, or skill definitions.
* Live credentials live ONLY in `$HARNESS_HOME/antigravity-accounts.json`, which is gitignored. Use `antigravity-accounts.example.json` as the schema template.
* If the security agent detects a secret-like string in any agent output, it MUST halt the loop and emit a high-priority vulnerability notification.
