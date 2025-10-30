import os
import json
import subprocess
import sys
import tempfile

SANITISER_ERROR = 2

test_env_vars = {
    "ASAN_OPTIONS": f"print_summary=1:verbosity=0:exitcode={SANITISER_ERROR}"
}

def extract_sanitiser_summary(sanitiser_summary: str) -> str:
    """
    Sanitisers will print a lot of hard-to-read junk so this function collects
    the line that starts with SUMMARY:
    """
    prefix = "SUMMARY:"
    return next((line.removeprefix(prefix).strip() for line in sanitiser_summary.splitlines() if line.startswith(prefix)), "")

def run_tests(test_executable: str, tests: list[object]):
    for test in tests:
        # Get testcase ID to run test runner.
        id = test["id"]
        if "name" not in test:
            test["name"] = id
        
        # Set initial conditions.
        test["ok"] = True
        test["passed"] = False

        # Run test.
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as temp:
            out = subprocess.run(
                [test_executable, f"--gtest_filter={id}", f"--gtest_output=json:{temp.name}"],
                env={**os.environ, **test_env_vars},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if out.returncode == SANITISER_ERROR:
                test["feedback"] = extract_sanitiser_summary(out.stderr.decode("utf-8", errors="replace"))
                continue

            if out.returncode not in (0, 1):
                if "observed" not in test or test["observed"] == "":
                    test["feedback"] = "Uncaught runtime error"
                    continue

            testworld_detail = json.load(temp)
            testsuite_detail = testworld_detail["testsuites"][0]
            testcase_detail = testsuite_detail["testsuite"][0]
            test["passed"] = not testsuite_detail["failures"]
            if "score" in testcase_detail:
                test["score"] = float(testcase_detail["score"])
            if "expected" in testcase_detail:
                test["expected"] = testcase_detail["expected"]
            if "observed" in testcase_detail:
                test["observed"] = testcase_detail["observed"]
            if "failures" in testcase_detail:
                test["feedback"] = testcase_detail["failures"][0]["failure"]
    return tests

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: run_tests.py <test_executable> <test_input> [output_file]", file=sys.stderr)
        sys.exit(1)

    test_executable = sys.argv[1]
    test_input = sys.argv[2]

    tests = json.load(open(test_input, "r"))
    result = run_tests(test_executable, tests)
    output = json.dumps(result)

    # Write JSON to output file if provided.
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
        with open(output_file, "w") as f:
            f.write(output)

    print(output)