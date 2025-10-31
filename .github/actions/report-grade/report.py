import json

from actions_toolkit import core

results = core.get_input("results")

print("DEBUGGING", results)

results2 = core.get_multiline_input("results")
print("DEBUGGING", results2)


for result in results:
    with open(result, "r") as f:
        res = json.load(f)
        print(res)
        core.notice(res)