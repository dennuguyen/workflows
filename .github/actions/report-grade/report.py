import json
import os

from actions_toolkit import core

results = os.getenv("INPUT_RESULTS", "")
results = [r.strip() for r in results.split(",")]

print("DEBUGGING", results)

for result in results:
    with open(result, "r") as f:
        res = json.load(f)
        print(res)
        core.notice(res)