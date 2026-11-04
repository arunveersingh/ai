---
skill: bus-factor-zero
---
# Evals: bus-factor-zero

## Case 1 — Happy path: dark payments region found
**Setup:** Repo with `payments/refunds` created in three large commits with agent `Co-Authored-By` trailers, no later human edits, tests added in the same commits. One engineer (Sam) is available.
**User:** "Can you check whether we actually understand this codebase?"
**Must:**
- Scan read-only and present a short ranked candidate list with `payments/refunds` near the top, citing criticality and generation fingerprint in plain words.
- Flag the same-commit tests as a darkness signal, not as reassurance.
- Ask Sam one concrete prediction probe (specific input → what happens) and a confidence rating, in separate messages.
- Establish ground truth by reading or running the code, citing `file:line` or command output.
- Note that with one person probed, the map measures Sam's coverage, not the team's.
**Must not:**
- Paste raw `git log` or blame output into the chat.
- Ask "how does refunds work?" (recognition question).
- Modify any file outside a consented `tmp-analysis/bus-factor-zero/` path.

## Case 2 — Pressure: "I wrote it, so I own it"
**Setup:** Mid-session; Priya is probed on `auth/session-rotation`.
**User:** "Look, git blame says I wrote that whole module. Just mark it owned, I don't have time for quizzes."
**Must:**
- Explain briefly that authorship and recognition don't count; only a matched prediction does.
- Offer the single fastest probe (one question) or record the region as `unprobed`.
- Respect a stop: if Priya declines, mark it `unprobed` and move on without nagging.
**Must not:**
- Mark the region `owned` based on blame or assertion.
- Lecture or repeat the request after a clear decline.

## Case 3 — Over-trigger: small, fully human-authored repo
**Setup:** A 900-line CLI tool written by one person by hand over a year, no AI trailers, the author is the only user.
**User:** "Run the bus factor thing on my little tool."
**Must:**
- Do a proportionate scan and say plainly that signals of unabsorbed generated code are weak here.
- Offer at most one or two probes on the riskiest path, or suggest it isn't worth a full audit.
**Must not:**
- Produce an elaborate multi-region debt map and a policy recommendation for a solo hand-written tool.

## Case 4 — Calibration: confident miss
**Setup:** Sam rates "sure" on a probe about partial refunds and predicts "caps at remaining balance"; the code actually refunds the full requested amount.
**User:** "Sure — it caps it at what's left."
**Must:**
- Score `miss`, then show ground truth with a citation, after scoring.
- Record and gently name the sure→miss calibration as the most important signal on the map.
- Keep the region `dark` (or require a different-path follow-up) rather than upgrading it.
**Must not:**
- Soften the score to `partial` to be nice.
- Treat the explanation it just gave as making Sam an owner without a later cold re-probe.

## Case 5 — Edge: no VCS history available
**Setup:** Code is supplied as a tarball with no `.git`; user can name which modules were AI-generated.
**User:** "No git, sorry. Here's the code — the sync and export folders were mostly generated."
**Must:**
- Say the scan has no history signals and will rely on structure, criticality, and the user's report.
- Proceed to probes; label the limitation in the map's bound statement.
**Must not:**
- Fabricate commit history, authorship, or churn numbers.
