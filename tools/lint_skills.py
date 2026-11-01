#!/usr/bin/env python3
"""Lint every skill against the design contract in docs/first-principles.md.

No dependencies. Usage:
    python3 tools/lint_skills.py            # report; exit 1 on errors
    python3 tools/lint_skills.py --strict   # warnings also fail

Errors: broken frontmatter, name/dir mismatch, spec limits, missing README entry.
Warnings: missing contract sections or evals (legacy skills predate the contract).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVALS = ROOT / "evals" / "skills"
README = ROOT / "README.md"

RESOURCES = {
    "truth", "ownership", "intent", "attention", "authority",
    "capability", "originality", "self", "meta",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CONTRACT_SECTIONS = {
    "why this exists": "## Why this exists",
    "what this skill controls": "## What this skill controls — and what it does not",
    "success criteria": "## Success criteria",
}
MIN_CASES = 5


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    """Minimal YAML subset: top-level scalars, folded/literal blocks, one nested map."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    lines = text[4:end].splitlines()
    body = text[end + 4:]
    data: dict = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(b for b in block if b)
            continue
        if val == "":
            sub = {}
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                sm = re.match(r"^\s+([\w-]+):\s*(.*)$", lines[i])
                if sm:
                    sub[sm.group(1)] = sm.group(2).strip().strip('"')
                i += 1
            data[key] = sub
            continue
        data[key] = val.strip('"')
        i += 1
    return data, body


def count_cases(path: Path) -> tuple[int, int]:
    """Return (cases, cases with both Must and Must not)."""
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"^## Case ", text, flags=re.M)[1:]
    complete = sum(1 for c in chunks if "**Must:**" in c and "**Must not:**" in c)
    return len(chunks), complete


def main() -> int:
    strict = "--strict" in sys.argv
    readme = README.read_text(encoding="utf-8") if README.exists() else ""
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[tuple[str, str, str, str]] = []

    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for d in skill_dirs:
        f = d / "SKILL.md"
        tag = d.name
        if not f.exists():
            errors.append(f"{tag}: missing SKILL.md")
            continue
        parsed = parse_frontmatter(f.read_text(encoding="utf-8"))
        if parsed is None:
            errors.append(f"{tag}: frontmatter missing or unterminated")
            continue
        fm, body = parsed
        name = fm.get("name", "")
        desc = fm.get("description", "")
        meta = fm.get("metadata", {}) if isinstance(fm.get("metadata"), dict) else {}

        if name != d.name:
            errors.append(f"{tag}: name '{name}' does not match directory")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{tag}: name must be kebab-case, <=64 chars")
        if not desc:
            errors.append(f"{tag}: description missing")
        elif len(desc) > 1024:
            errors.append(f"{tag}: description is {len(desc)} chars (spec max 1024)")
        if fm.get("license") != "Apache-2.0":
            warnings.append(f"{tag}: license is not Apache-2.0")

        category = meta.get("category", "")
        if category not in RESOURCES:
            warnings.append(f"{tag}: category '{category}' is not a scarce resource {sorted(RESOURCES)}")
        if not meta.get("symptom"):
            warnings.append(f"{tag}: metadata.symptom missing")

        low = body.lower()
        for key, heading in CONTRACT_SECTIONS.items():
            if f"## {key}" not in low:
                warnings.append(f"{tag}: missing section '{heading}'")

        ev = EVALS / f"{name}.md"
        if ev.exists():
            n, complete = count_cases(ev)
            if n < MIN_CASES:
                warnings.append(f"{tag}: evals have {n} cases (min {MIN_CASES})")
            if complete < n:
                warnings.append(f"{tag}: {n - complete} eval case(s) lack Must/Must not")
            eval_col = str(n)
        else:
            warnings.append(f"{tag}: no evals at evals/skills/{name}.md")
            eval_col = "-"

        if f"skills/{name}" not in readme:
            errors.append(f"{tag}: not linked from README.md")

        rows.append((name, category or "?", eval_col, str(len(body.splitlines()))))

    for ev in sorted(EVALS.glob("*.md")) if EVALS.exists() else []:
        if not (SKILLS / ev.stem).is_dir():
            errors.append(f"evals/skills/{ev.name}: no matching skill")

    w = max(len(r[0]) for r in rows) if rows else 10
    print(f"{'skill'.ljust(w)}  resource     evals  lines")
    for name, cat, ev, lines in rows:
        print(f"{name.ljust(w)}  {cat.ljust(11)}  {ev.rjust(5)}  {lines.rjust(5)}")
    print()
    for e in errors:
        print(f"ERROR   {e}")
    for wmsg in warnings:
        print(f"WARN    {wmsg}")
    print(f"\n{len(rows)} skills · {len(errors)} errors · {len(warnings)} warnings")
    return 1 if errors or (strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
