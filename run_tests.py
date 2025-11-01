import os
import json
import subprocess
import sys
import tempfile

from testing_model import TestSuite

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

def run_tests(test_executable: str, suite: TestSuite) -> TestSuite:
    for test in suite.tests:
        test.passed = False

        # Run test.
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as temp:
            out = subprocess.run(
                [test_executable, f"--gtest_filter={test.id}", f"--gtest_output=json:{temp.name}"],
                env={**os.environ, **test_env_vars},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if out.returncode == SANITISER_ERROR:
                test.feedback = extract_sanitiser_summary(out.stderr.decode("utf-8", errors="replace"))
                continue

            if out.returncode not in (0, 1):
                if "observed" not in test or test["observed"] == "":
                    test.feedback = "Uncaught runtime error"
                    continue

            # Get to relevant data from test output.
            testworld_detail = json.load(temp)
            testsuite_detail = testworld_detail["testsuites"][0]
            testcase_detail = testsuite_detail["testsuite"][0]

            # Get runtime metadata from running tests.
            test.passed = not testsuite_detail["failures"]
            test.score = testcase_detail.get("score", test.score)
            test.penalty = testcase_detail.get("penalty", test.penalty)
            test.hidden = testcase_detail.get("hidden", False)
            test.secret = testcase_detail.get("secret", False)
            test.expected = testcase_detail.get("expected", None)
            test.observed = testcase_detail.get("observed", None)
            if "failures" in testcase_detail:
                test.feedback = testcase_detail["failures"][0]["failure"]
    return suite

def normalise_scores(suite: TestSuite) -> TestSuite:
    """
    Re-adjust scores and penalties.
    """
    for test in suite.tests:
        if test.penalty:
            test.penalty = test.penalty or -1
            test.penalty = -abs(test.penalty)
            suite.score += test.penalty
        else:
            test.score = test.score or 1
            suite.score += test.score
            suite.max_score += test.score
    return suite

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: run_tests.py <test_executable> <test_configuration> [output_file]", file=sys.stderr)
        sys.exit(1)

    test_exec = sys.argv[1]
    test_conf = sys.argv[2]

    suite = TestSuite(**json.load(open(test_conf, "r")))
    suite = run_tests(test_exec, suite)
    suite = normalise_scores(suite)
    output = suite.model_dump_json()

    # Write JSON to output file if provided.
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
        with open(output_file, "w") as f:
            f.write(output)

    print(output)