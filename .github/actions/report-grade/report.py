import difflib
import json
import sys

from actions_toolkit import core
from colorama import Fore, Back, Style

def diff(text1: str, text2: str) -> str:
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    colored_output = []
    for line in diff:
        if line.startswith('+'):
            colored_output.append(f"{Back.GREEN}{line}{Style.RESET_ALL}")
        elif line.startswith('-'):
            colored_output.append(f"{Back.RED}{line}{Style.RESET_ALL}")
        else:
            colored_output.append(line)
    return "\n".join(colored_output)

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

    if passed:
        print(f"{Fore.GREEN}✅ {name} ({score}/{max_score}){Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}❌ {name} ({score}/{max_score}){Style.RESET_ALL}")
        core.start_group("Feedback")
        print(f"{feedback}")
        print(f"Difference was:")
        print(diff(expected, observed))
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