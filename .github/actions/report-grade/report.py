from actions_toolkit import core

results = core.get_multiline_input("results")

for result in results:
    core.info(str(result))