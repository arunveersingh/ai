---
name: parse-or-reject
description: Day 10 practice — parsed is not valid. When code reads model output, lenient parsing turns a wrong reply into a wrong value with no error (a decimal comma shrinks a refund 1,000 times, a missing amount becomes zero). Define the exact shape, make missing a legal null, tie values to their source, and let a validator accept or reject. Rejected output is retried once with the errors, then sent to a person, never repaired.
---

# Parse or reject

A model reads refund emails and drafts refunds. The email says "1.250,00 EUR"; the reply copies it; the code strips the comma and refunds 1.25. Another email has no amount; `.get("amount", "0")` drafts a zero refund. No error either time.

Parsed is not valid. If your code can always turn the reply into a value, it will turn a wrong reply into a wrong value. The fix: the model writes, a validator decides.

## Part A — Ask (paste and adapt)

```
Reply with one JSON object and nothing else. Exactly these keys:
order_id: "A-" followed by digits, as written in the email
amount: like "1250.00" (dot decimal, two places, no separators), or null
currency: "EUR", "GBP" or "USD", or null
amount_text: the amount exactly as written in the email, or null
reason: "duplicate_charge", "not_received", "damaged" or "other"
If the email states no amount, amount, currency and amount_text are null.
Never estimate. A program checks this reply and rejects anything else.
```

**In an orchestrated flow** (spec → plan → tasks → implement): the schema and reject path go in the spec as requirements; the validator task comes before the prompt task. Validate agent replies your scripts act on (headless runs, subagent reports) the same way.

## Part B — Validate (you do this)

[`validate.py`](./validate.py) has no dependencies. Adapt `FIELDS` to your output and keep its rules:

1. **Exact keys.** Missing or extra keys reject.
2. **A format per value.** A pattern or a fixed list, not just a type.
3. **Missing is null, never a default.** A null record goes to a person.
4. **Tie values to the source.** A quoted span must appear in the input.
5. **On reject:** send the reply back once with the error list. Still rejected → a person. Never fix it up in code.

```bash
python3 validate.py reply.json email.txt   # exit 0 accepted, 1 rejected
```

**Limit:** it checks only what you encode. A well-shaped, sourced misreading (`"1.25"` from `"1.250,00 EUR"`) passes, so check money against your own records too.

**Done when:** the validator rejects at least one real or hand-broken reply, and no rejected reply can reach the next step.

Lesson: [Day 10 — Parse or Reject](../../day-10.md)
