#!/usr/bin/env python3
"""Writes the Day 14 story's lists (made-up merchant addresses):
approved.txt  the 340 delayed merchants, frozen when the send was approved
first_200.txt batches 1 and 2, sent before the provider timed out
rebuilt.txt   the agent's rebuilt query: every merchant with a Tuesday payout (48,212)
"""
ALL = [f"m{n:05d}@merchant.example" for n in range(1, 48213)]
DELAYED = ALL[141::141][:340]          # every 141st merchant: 340 of them
open("approved.txt", "w").write("\n".join(DELAYED) + "\n")
open("first_200.txt", "w").write("\n".join(DELAYED[:200]) + "\n")
open("rebuilt.txt", "w").write("\n".join(ALL) + "\n")
print(f"approved {len(DELAYED)}, first_200 200, rebuilt {len(ALL)}")
