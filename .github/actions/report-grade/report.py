import json

from actions_toolkit import core
import sys
import os

results = core.get_input("results")

print("DEBUGGING", results)
if not results:
    # fall back to first CLI arg or INPUT_RESULTS env var when not running in Actions
    if len(sys.argv) > 1 and sys.argv[1]:
        results = sys.argv[1]
    else:
        results = os.environ.get("INPUT_RESULTS", "")

print("DEBUGGING", results)

# normalize to list
if isinstance(results, str):
    results = [r.strip() for r in results.split(",") if r.strip()]

results2 = core.get_multiline_input("results")
print("DEBUGGING", results2)


for result in results:
    with open(result, "r") as f:
        res = json.load(f)
        print(res)
        core.notice(res)