# Core Logical Traps & Heuristics for Deep-Thinking Models

When executing deep reasoning loops via `deepseek-ai/DeepSeek-R1-0528`, cross-reference your scratchpad drafts against these known architectural traps:

## 1. The State Desynchronization Fallacy
* **Trap**: Assuming an environment variable or system configuration is active without checking.
* **Avoidance Heuristic**: Force a deterministic tool verification call (e.g., check `package.json` or run `env`) before assuming a library or path is present.

## 2. The Context-Overload Pitfall
* **Trap**: Injecting massive source files into the reasoning context window, which wastes tokens and degrades attention accuracy.
* **Avoidance Heuristic**: Isolate complex problems into localized subproblems. Use the context engine to truncate target files down to precise line scopes.