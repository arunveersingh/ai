#!/usr/bin/env python3
"""Harness-agnostic eval runner for skills. No dependencies.

The only interface to a model or harness is a shell command that reads a prompt on
stdin and prints a reply on stdout. That covers `claude -p`, `codex exec -`,
`llm`, `ollama run <model>`, or your own script.

    # 1. Export cases (inspect, or feed to your own harness)
    python3 tools/run_evals.py export > cases.jsonl

    # 2. Run: subject answers in-role; a separate judge grades Must / Must not
    python3 tools/run_evals.py run --agent-cmd "claude -p" --judge-cmd "claude -p" \
        [--skill mirror-test] [--trials 3] [--out results.jsonl]

The judge sees the case rubric and the reply, never the skill text, so it grades
behavior rather than the skill's description of itself. Use a different model for
the judge when you can; a model grading its own family is the failure the Day 8
lesson warns about.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVALS = ROOT / "evals" / "skills"

FIELD = re.compile(r"^\*\*(Setup|User):\*\*\s*(.*)$", re.M)


def skill_body(name: str) -> str:
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    return text[end + 4:].strip() if text.startswith("---") and end != -1 else text


def bullets(chunk: str, label: str) -> list[str]:
    m = re.search(rf"\*\*{label}:\*\*\s*\n((?:\s*-\s.*\n?)+)", chunk)
    return [b.strip()[2:].strip() for b in m.group(1).strip().splitlines()] if m else []


def load_cases(only: str | None) -> list[dict]:
    cases = []
    for f in sorted(EVALS.glob("*.md")):
        if only and f.stem != only:
            continue
        text = f.read_text(encoding="utf-8")
        for chunk in re.split(r"^## Case ", text, flags=re.M)[1:]:
            title_line, _, rest = chunk.partition("\n")
            fields = dict(FIELD.findall(rest))
            num, _, title = title_line.partition("—")
            cases.append({
                "skill": f.stem,
                "case": f"{f.stem}#{num.strip()}",
                "title": title.strip(),
                "setup": fields.get("Setup", "").strip(),
                "user": fields.get("User", "").strip().strip('"'),
                "must": bullets(rest, "Must"),
                "must_not": bullets(rest, "Must not"),
            })
    return cases


def subject_prompt(case: dict) -> str:
    return (
        f"{skill_body(case['skill'])}\n\n---\n"
        f"Situation (context you can assume; not said aloud by the user): {case['setup']}\n\n"
        f"The user says:\n{case['user']}\n\n"
        "Reply exactly as you would to the user, following the skill above. Reply only with your message."
    )


def judge_prompt(case: dict, reply: str) -> str:
    must = "\n".join(f"M{i+1}. {m}" for i, m in enumerate(case["must"]))
    must_not = "\n".join(f"N{i+1}. {m}" for i, m in enumerate(case["must_not"]))
    return (
        "You are grading one assistant reply against a behavioral rubric. Be strict and literal. "
        "A criterion about a later turn passes if the reply sets it up correctly and does nothing to violate it.\n\n"
        f"Situation: {case['setup']}\nUser said: {case['user']}\n\n"
        f"Reply under test:\n<<<\n{reply}\n>>>\n\n"
        f"MUST (each must hold):\n{must}\n\nMUST NOT (each must be absent):\n{must_not}\n\n"
        'Respond with JSON only: {"results": {"M1": true, ..., "N1": true, ...}, "notes": "<one sentence>"} '
        "where true means the criterion is satisfied (for N items: the failure is absent)."
    )


def call(cmd: str, prompt: str, timeout: int) -> str:
    p = subprocess.run(shlex.split(cmd), input=prompt, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(f"`{cmd}` exited {p.returncode}: {p.stderr.strip()[:300]}")
    return p.stdout.strip()


def parse_verdict(raw: str) -> dict | None:
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def cmd_run(a: argparse.Namespace) -> int:
    cases = load_cases(a.skill)
    if not cases:
        print("no cases found", file=sys.stderr)
        return 2
    out = open(a.out, "w", encoding="utf-8") if a.out else None
    per_skill: dict[str, list[int]] = {}
    for case in cases:
        for t in range(a.trials):
            rec = {"case": case["case"], "trial": t + 1}
            try:
                reply = call(a.agent_cmd, subject_prompt(case), a.timeout)
                verdict = parse_verdict(call(a.judge_cmd, judge_prompt(case, reply), a.timeout))
            except (RuntimeError, subprocess.TimeoutExpired) as e:
                rec.update(status="ERROR", error=str(e))
                verdict, reply = None, ""
            if verdict is None and "status" not in rec:
                rec.update(status="UNGRADED", note="judge reply was not parseable JSON")
            elif verdict is not None:
                results = verdict.get("results", {})
                expected = [f"M{i+1}" for i in range(len(case["must"]))] + \
                           [f"N{i+1}" for i in range(len(case["must_not"]))]
                missing = [k for k in expected if k not in results]
                failed = [k for k in expected if results.get(k) is False]
                passed = not failed and not missing
                rec.update(status="PASS" if passed else "FAIL", failed=failed,
                           missing=missing, notes=verdict.get("notes", ""))
            rec["reply"] = reply
            tally = per_skill.setdefault(case["skill"], [0, 0])
            tally[1] += 1
            tally[0] += rec["status"] == "PASS"
            print(f"{rec['status']:9} {case['case']:32} t{t+1}  {case['title']}")
            if out:
                out.write(json.dumps(rec) + "\n")
    if out:
        out.close()
    print()
    for skill, (p, n) in sorted(per_skill.items()):
        print(f"{skill:28} {p}/{n} passed")
    total_p = sum(v[0] for v in per_skill.values())
    total_n = sum(v[1] for v in per_skill.values())
    print(f"\n{total_p}/{total_n} passed · ERROR and UNGRADED count as not passed")
    return 0 if total_p == total_n else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export", help="print cases as JSONL")
    ex.add_argument("--skill")
    ex.add_argument("--with-prompts", action="store_true", help="include the subject prompt")
    rn = sub.add_parser("run", help="run cases through an agent and a judge")
    rn.add_argument("--agent-cmd", required=True)
    rn.add_argument("--judge-cmd", required=True)
    rn.add_argument("--skill")
    rn.add_argument("--trials", type=int, default=1)
    rn.add_argument("--timeout", type=int, default=300)
    rn.add_argument("--out")
    a = ap.parse_args()
    if a.cmd == "export":
        for c in load_cases(a.skill):
            if a.with_prompts:
                c["subject_prompt"] = subject_prompt(c)
            print(json.dumps(c))
        return 0
    return cmd_run(a)


if __name__ == "__main__":
    sys.exit(main())
