import json
import sys

from actions_toolkit import core

if len(sys.argv) < 2:
    print("Usage: report.py <result_files>", file=sys.stderr)
    sys.exit(1)

results = sys.argv[1]
results = [r.strip() for r in results.split(",")]

print("DEBUGGING", results)

for result in results:
    with open(result, "r") as f:
        res = json.load(f)
        print(res)
        core.notice(res)