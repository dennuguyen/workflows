import json

from actions_toolkit import core

results = core.get_input("results")

print("DEBUGGING", results)

for result in results:
    with open(result, "r") as f:
        res = json.load(f)
        print(res)
        core.notice(res)