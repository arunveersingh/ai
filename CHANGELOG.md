# Changelog

## 2.0 — The scarcity redesign (Nov 2026)

The repo is reorganized around one principle: AI made producing work nearly free, so the work that still matters is protecting what stayed scarce (truth, ownership, intent, attention, authority, capability, originality, self).

**Added**
- 13 skills: `symptom-triage`, `mirror-test`, `commit-then-consult`, `perception-gap-auditor`, `define-good-first`, `bus-factor-zero`, `delegation-contract`, `attention-treasurer`, `workslop-interceptor`, `capability-reserve`, `modal-escape`, `human-bridge`, `value-relocator`
- `docs/symptom-atlas.md`: research on how people struggle with AI, with evidence grades and sources
- `docs/first-principles.md`: the underlying thesis, the design contract, and the recurring mechanisms
- `evals/`: behavioral cases for every skill, plus `tools/run_evals.py`, a harness-agnostic runner that uses any stdin→stdout model command
- `tools/lint_skills.py`: checks every skill against the design contract

**Changed**
- Every skill is categorized by the scarce resource it protects and declares the symptom it targets
- Existing skills (v1.1, and recontextualizer v1.3) gained a "Why this exists" section, honest wording about what they can and can't enforce (a prompt cannot block an owner), a "What this skill controls" section, and evals
- README rewritten around the eight scarce resources, with `symptom-triage` as the entry point
