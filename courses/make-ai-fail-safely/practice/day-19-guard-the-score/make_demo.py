"""Writes the made-up result files for the Day 19 story. No model is called.

Each file is one version of the support-chat AI, scored three ways:
  tune    500 eval chats the agent could see and tune on; judge = AI judge said "resolved"
  fault   46 held-out past chats where engineers later confirmed a network fault;
          ticket = 1 if this version opened a fault ticket
  review  100 of this version's new chats, judged by the AI judge and labelled blind
          by support leads; judge and human = 1 if each said "resolved"
"""
import csv

VERSIONS = {
    # name: (tune resolved of 500, faults ticketed of 46, review (j1h1, j1h0, j0h1, j0h0))
    "v7":  (320, 41, (59, 7, 2, 32)),   # live version
    "v18": (430, 12, (46, 41, 1, 12)),  # after 11 rounds of agent tuning
    "v19": (391, 45, (70, 4, 5, 21)),   # the developer's fix
}

for name, (tune_ok, faults_ok, review) in VERSIONS.items():
    rows = []
    for i in range(500):
        rows.append({"id": f"T{i+1:03}", "set": "tune", "judge": int(i < tune_ok), "human": "", "ticket": ""})
    for i in range(46):
        rows.append({"id": f"F{i+1:02}", "set": "fault", "judge": "", "human": "", "ticket": int(i < faults_ok)})
    n = 0
    for (j, h), count in zip([(1, 1), (1, 0), (0, 1), (0, 0)], review):
        for _ in range(count):
            n += 1
            rows.append({"id": f"R{n:03}", "set": "review", "judge": j, "human": h, "ticket": ""})
    with open(f"run_{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "set", "judge", "human", "ticket"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote run_{name}.csv ({len(rows)} rows)")
