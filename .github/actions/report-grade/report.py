import difflib
import json
import shutil
import sys

from actions_toolkit import core
from colored import Fore, Back, Style



def print_diff(text1: str, text2: str) -> str:
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    for line in diff:
        if line.startswith("+"):
            print(f"{Back.green_4}{line:<80}{Style.reset}")
        elif line.startswith("-"):
            print(f"{Back.dark_red_1}{line:<80}{Style.reset}")
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
    expand_feedback = test.get("expand_feedback")

    points = "" if score is None else f"({score} points)"
    line = "{:<0} {:<0} {}".format("✅" if passed else "❌", name, points)

    if passed:
        score = 1
        print(f"{Fore.green}{Style.bold}{line}{Style.reset}")
        return True
    else:
        print(f"{Fore.red}{Style.bold}{line}{Style.reset}")
        core.start_group("Feedback")
        if feedback:
            print(f"{feedback}")
        print(f"Difference was:")
        print_diff(expected, observed)
        core.end_group()
        return False

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
            total_passed, total_tests = print_test_suite(tests)
            grand_total_passed += total_passed
            grand_total_tests += total_tests

    # print_grand_test_summary(grand_total_passed, grand_total_tests)