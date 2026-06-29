# Benchmarks

Drop benchmark scripts and golden datasets here. Each benchmark must:
1. Load a dataset from `evaluations/datasets/<name>.json`.
2. Replay the dataset through the orchestrator.
3. Write a JSON report to `evaluations/reports/<dataset-id>-<timestamp>.json`.

See `evaluations/metrics.schema.json` for the metrics contract.
