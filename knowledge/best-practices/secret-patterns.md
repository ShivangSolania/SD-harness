# Secret Patterns (extensible)

Drop regex patterns here to extend `agents/security.md`'s secret scanner.
One pattern per line, format: `<name>\t<regex>`.

Example:
```
aws-access-key	AKIA[0-9A-Z]{16}
github-token	gh[pousr]_[A-Za-z0-9]{36,}
```

If this file is empty, the security agent falls back to its built-in heuristics.
