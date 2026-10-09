---
name: as-of-or-stop
description: Day 7 practice — stop trusting the model's memory about anything that changes. Give it today's date and the lockfile, make every changeable claim carry "as of <date>" and a source, label memory-only claims FROM MEMORY, stop when there is no live source, and add dependencies through the package manager. Then grep for undated "latest" claims, audit the lockfile against today's advisories, run the audit in CI on PRs and nightly, and inject the date in code.
---

# As of, or stop

You ask your agent to pin the latest `requests`: lock it to one exact version so every install gets the same code. It writes `requests==2.31.0 (latest stable)`. That was true in 2023. On 9 Oct 2026 the newest is 2.34.2, and 2.31.0 has three known advisories. Nothing errors and the tests pass.

Known then is not true now. The fix has two parts. **Ask:** anything that can change needs a date and a live source, memory alone means stop, and versions come from the package manager. **Verify:** flag undated claims, and let an audit against today's advisory data decide "safe."

Paste Part A into the agent's standing instructions or before the task. Do Part B yourself. Fill in the brackets.

## Part A — Ask (paste and adapt)

```
Today is [YYYY-MM-DD]. Installed versions: [paste lockfile or
"pip freeze"].
1. For anything that can change over time (versions, prices,
   limits, API behavior, people in roles), write:
   as of <date>, source: <tool output or URL>
2. If your only source is training data, write FROM MEMORY.
   Don't act on it.
3. If you have a lookup tool, run it and quote the output.
   If not, write STOPPED: no live source. You may propose
   one lookup.
4. Add dependencies with the package manager. Report the version
   it installed. Never type a version number from memory.
```

**Adapting it:** for npm, Maven, or Go, swap in that package manager and lockfile. For non-code facts (pricing, rate limits, org charts), the source is a URL or document with its own date; "as of" is the date of that source, not today.

## Part B — Verify (you do this)

1. **Flag undated claims.** Reply saved as `reply.txt`:
   `! grep -nEi '\b(latest|current|newest|up to date)\b' reply.txt | grep -viE 'as of [0-9]{4}|FROM MEMORY'`
   It prints any "latest" line with no date or label and fails if there is one.
2. **Audit the lockfile.** Pin everything, including sub-dependencies (`pip freeze > requirements.txt` or pip-compile), then `pip-audit -r requirements.txt`. Exit 0 = no known advisory today. Exit 1 = advisory found, or the database couldn't be reached (fails closed). No saved state, so it works the same on a fresh machine.
3. **Let CI decide, on PRs and nightly.** Require the audit on PRs and run it on a schedule, so advisories published after merge still surface. Multi-module or mixed stacks: `osv-scanner scan source -r .` audits every standard lockfile under the repo in one run; exit 128 if it finds none. Ignore an advisory only with its ID and reason in a reviewed commit. Don't gate on "newest version": it flakes every release.
4. **Inject the date in code.** If you build the agent, put today's date and the current lockfile in the system prompt on every run, and give it a version-lookup tool.

**Done when:** the template returns FROM MEMORY or STOPPED for a "latest" question without a live source, the grep passes on its replies, and the audit (or a written plan for one) runs in CI on PRs and nightly.

Lesson: [Day 7 — Stale Certainty](../../day-07.md)
