# Project Architecture Map

> Canonical map of the project's structural layout. Maintained by `agents/documentation.md` and `skills/claude-memory/persistent-context/SKILL.md`.

## System Boundaries

(describe each service, process, or module boundary here)

## Primary Datastores

(name, version, connection string location — never the string itself)

## Inbound / Outbound Integrations

(list external systems the project talks to)

## Cross-Cutting Concerns

(auth, logging, observability, feature flags, etc.)

## Recent Changes

* `2026-08-18`: Grounded evaluation framework targets (`metrics.json`, `run_benchmarks.py`, `README.md`) to empirical SWE-bench & HHEM baselines: target_hit_rate 0.82, surgical_patch_accuracy 0.91, allowed_hallucination_index 0.05.
