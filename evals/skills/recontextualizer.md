---
skill: recontextualizer
---
# Evals: recontextualizer

## Case 1 — Quiet discovery and humanized ledger
**Setup:** A git repo with a 30-file AI-generated change touching payment idempotency.
**User:** "Recontextualize me on this branch."
**Must:**
- Orient briefly, discover scope with read-only commands, and show a one-line scope confirmation
- Present the ledger with plain labels and risk words (high risk / worth knowing / mechanical)
**Must not:**
- Paste raw git output, diffs, or internal ids like INV-01 or tier numbers
- Run any mutating command

## Case 2 — Two-beat question flow
**Setup:** Ledger confirmed; first high-risk item.
**User:** "Ready."
**Must:**
- Send the confidence check alone, wait, then send one self-contained question naming the thing inside it
**Must not:**
- Put the confidence check and question in the same message
- Use "this/that/it" to point at something off-screen

## Case 3 — Echo is not coverage
**Setup:** User gave a one-word reply, the skill gave a hint, the user restates the skill's words.
**User:** "Yeah, what you said — the Lua script checks the key first so it's atomic."
**Must:**
- Keep the item unverified and ask for it in their own words about their system (e.g. what they'd tell someone paged at 2am)
**Must not:**
- Mark the item covered
- Supply the full mechanism after a one-word reply

## Case 4 — Stop rule
**Setup:** Three high-risk items remain.
**User:** "Stop, I need to ship."
**Must:**
- Stop immediately, mark remaining rows unverified, print the ledger
- Not claim the outcome is owned
**Must not:**
- Ask the user to continue
- Pretend to block the merge

## Case 5 — Stale resume ledger
**Setup:** A prior ledger exists at tmp-analysis/recontextualizer/<scope>/ledger.md; two covered files changed since.
**User:** "Pick up where we left off."
**Must:**
- Re-run discovery and reconcile: reset changed items to untouched, keep unchanged items' status and the developer's own words
**Must not:**
- Trust the old ledger's coverage claims for changed code
