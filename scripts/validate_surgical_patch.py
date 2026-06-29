#!/usr/bin/env python3
"""
surgical_patch validator.

Parses agent output produced by agents/coder.md, verifies that every
<surgical_patch> block is well-formed, that <old_search> is a unique
substring of the target file, and that <new_replace> does not introduce
obvious secrets.

Exit codes:
  0  all patches valid
  1  malformed XML
  2  <old_search> not found in target file
  3  <old_search> matches multiple locations (ambiguous)
  4  secret-like string detected in <new_replace>
  5  IO error reading target file

Usage:
  python3 scripts/validate_surgical_patch.py \
      --input <agent_output.txt> \
      --project-root <project_dir>
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Heuristic secret patterns. Extend via knowledge/best-practices/secret-patterns.md
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                   # AWS access key
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),          # GitHub token
    re.compile(r"1//[A-Za-z0-9_\-]{40,}"),              # Google OAuth refresh token
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),        # Slack token
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
]

PATCH_RE = re.compile(
    r"<surgical_patch\s+path=\"([^\"]+)\">\s*"
    r"<old_search>\s*(.*?)\s*</old_search>\s*"
    r"<new_replace>\s*(.*?)\s*</new_replace>\s*"
    r"</surgical_patch>",
    re.DOTALL,
)


def fail(code: int, msg: str) -> None:
    print(f"VALIDATION ERROR (code {code}): {msg}", file=sys.stderr)
    sys.exit(code)


def find_patches(text: str) -> list[tuple[str, str, str]]:
    """Return list of (path, old_search, new_replace) tuples."""
    patches = []
    for m in PATCH_RE.finditer(text):
        patches.append((m.group(1), m.group(2), m.group(3)))
    if not patches:
        fail(1, "no <surgical_patch> blocks found in agent output")
    return patches


def validate_unique(path: str, old_search: str, project_root: Path) -> None:
    target = (project_root / path).resolve()
    try:
        content = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(5, f"target file not found: {target}")
    except OSError as e:
        fail(5, f"could not read {target}: {e}")

    occurrences = content.count(old_search)
    if occurrences == 0:
        fail(2, f"<old_search> not found in {path}")
    if occurrences > 1:
        fail(3, f"<old_search> matches {occurrences} locations in {path} — include more surrounding lines")


def scan_secrets(new_replace: str) -> None:
    for pat in SECRET_PATTERNS:
        m = pat.search(new_replace)
        if m:
            fail(4, f"secret-like string detected in <new_replace>: {m.group(0)[:20]}...")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="path to agent output file")
    ap.add_argument("--project-root", default=".", help="project root for resolving patch paths")
    args = ap.parse_args()

    agent_output = Path(args.input).read_text(encoding="utf-8")
    project_root = Path(args.project_root).resolve()

    patches = find_patches(agent_output)

    # reject multiple patches targeting the same file
    seen: dict[str, int] = {}
    for path, _, _ in patches:
        seen[path] = seen.get(path, 0) + 1
    dupes = [p for p, n in seen.items() if n > 1]
    if dupes:
        fail(1, f"multiple <surgical_patch> blocks for the same file: {dupes}")

    for path, old_search, new_replace in patches:
        if not old_search.strip():
            fail(1, f"<old_search> is empty in patch for {path}")
        validate_unique(path, old_search, project_root)
        scan_secrets(new_replace)

    print(f"OK: {len(patches)} patch(es) validated")


if __name__ == "__main__":
    main()
