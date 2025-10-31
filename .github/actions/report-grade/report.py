from actions_toolkit import core

results = core.get_multiline_input("results")

for result in results:
    with open(result, "r") as f:
        core.info(f)