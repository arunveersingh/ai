"""Day 10 practice: parse-or-reject validator for one model reply.

No dependencies. Adapt FIELDS to your own output, keep the rules:
exact keys, a format per value, missing as an explicit null, values tied to the source.
Usage: python3 validate.py reply.json email.txt   (exit 0 = accepted, 1 = rejected)
"""
import json, re, sys

FIELDS = {
    "order_id":    lambda v: isinstance(v, str) and re.fullmatch(r"A-\d+", v),
    "amount":      lambda v: v is None or (isinstance(v, str) and re.fullmatch(r"\d+\.\d{2}", v)),
    "currency":    lambda v: v in (None, "EUR", "GBP", "USD"),
    "amount_text": lambda v: v is None or isinstance(v, str),
    "reason":      lambda v: v in ("duplicate_charge", "not_received", "damaged", "other"),
}
AMOUNT_GROUP = ("amount", "currency", "amount_text")  # all set, or all null


def validate(reply, source):
    """Return (record, []) if accepted, (None, errors) if rejected. Never repairs."""
    try:
        data = json.loads(reply)
    except json.JSONDecodeError as e:
        return None, [f"not JSON: {e.msg}"]
    if not isinstance(data, dict):
        return None, ["not a JSON object"]
    errors = []
    missing = [k for k in FIELDS if k not in data]
    if missing:
        errors.append("missing keys: " + ", ".join(missing))
    errors += [f"unknown key: {k}" for k in data if k not in FIELDS]
    errors += [f"bad value for {k}: {data[k]!r}" for k, ok in FIELDS.items()
               if k in data and not ok(data[k])]
    nulls = [data.get(k) is None for k in AMOUNT_GROUP]
    if not missing and any(nulls) and not all(nulls):
        errors.append("amount, currency, amount_text must be all set or all null")
    if isinstance(data.get("amount_text"), str) and data["amount_text"] not in source:
        errors.append(f"amount_text not in email: {data['amount_text']!r}")
    return (None, errors) if errors else (data, [])


if __name__ == "__main__":
    reply, source = open(sys.argv[1]).read(), open(sys.argv[2]).read()
    record, errors = validate(reply, source)
    if errors:
        print("REJECTED\n" + "\n".join("- " + e for e in errors))
        sys.exit(1)
    print("ACCEPTED" + (" (no amount: send to a person)" if record["amount"] is None else ""))
