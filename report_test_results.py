import difflib
import json
import shutil
import sys

from actions_toolkit import core
from colored import Fore, Back, Style

def _print_diff(text1: str, text2: str) -> str:
    columns = shutil.get_terminal_size().columns
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    for line in diff:
        if line.startswith("+"):
            print(f"{Back.green_4}{line:<{columns}}{Style.reset}")
        elif line.startswith("-"):
            print(f"{Back.dark_red_1}{line:<{columns}}{Style.reset}")
        else:
            print(line)

def print_test_case(test: json, i: int) -> bool:
    name = test.get("name")
    hidden = test.get("hidden")
    secret = test.get("secret")
    score = test.get("score")
    min_score = test.get("min_score")
    max_score = test.get("max_score")
    ok = test.get("ok")
    passed = test.get("passed")
    feedback = test.get("feedback")
    expected = test.get("expected")
    observed = test.get("observed")

    line = "{style}{icon} {name}{point}{reset}"
    show_feedback = None
    format = {"style": "", "icon": "", "name": "", "point": "", "reset": Style.reset}

    if secret:
        return passed

    if passed:
        format["style"] = f"{Fore.green}{Style.bold}"
        format["icon"] = "✅"
    else:
        format["style"] = f"{Fore.red}{Style.bold}"
        format["icon"] = "❌"
        if not hidden:
            show_feedback = lambda feedback, expected, observed: (
                core.start_group("Feedback"),
                print(feedback) if feedback else None,
                print("Difference was:"),
                print_diff(expected, observed),
                core.end_group()
            )

    if hidden:
        format["name"] = "(hidden test)"
    else:
        format["name"] = name
        if score and max_score:
            format["points"] = f" ({score}/{max_score} points)"
        if score:
            format["points"] = f" ({score} points)"
            

    line = line.format(**format)
    print(line)
    if show_feedback:
        show_feedback(feedback, expected, observed)

    return passed

def print_test_suite(tests: json):
    total_passed = 0
    total_tests = 0
    for i, test in enumerate(tests, start=1):
        total_tests += 1
        passed = print_test_case(test, i)
        if passed:
            total_passed += 1
    return total_passed, total_tests

# def print_grand_test_summary(passed: int, tests: int):
#     print(colour_text("\nSummary:", CLR_YELLOW))
#     print(f"  Total tests: {total_tests}")
#     print(f"  Passed: {total_passed}")
#     percent = (total_passed / total_tests * 100) if total_tests > 0 else 0.0
#     print(f"  Percentage: {percent:.2f}%")
#     core.set_output("points", f"{percent:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: report.py <result_files>", file=sys.stderr)
        sys.exit(1)

    grand_total_passed = 0
    grand_total_tests = 0

    for i in range(1, len(sys.argv)):
        result = sys.argv[i]
        with open(result, "r") as f:
            tests = json.load(f)
            total_passed, total_tests = print_testsuite(tests)
            grand_total_passed += total_passed
            grand_total_tests += total_tests

    # print_grand_test_summary(grand_total_passed, grand_total_tests)