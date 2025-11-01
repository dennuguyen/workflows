import re
import sys

from pathlib import Path
from pydantic import TypeAdapter
from testing_model import TestCase, TestSuite
from typing import List, Optional, Tuple

def _extract_metadata(line: str) -> Tuple[Optional[str], Optional[str]]:
    m = re.match(r"\/\/@(\w+)\s*(.*)", line)
    if m:
        key = m.group(1)
        value = m.group(2) or True
    return key, value

def _extract_testcase_metadata(code: List[str], row: int) -> TestCase:
    """
    Scans previous lines from the given line for testcase metadata.
    """
    row -= 1
    metadata = {}
    while row >= 0 and code[row].startswith("//@"):
        key, value = _extract_metadata(code[row])
        if key:
            metadata[key] = value
        row -= 1
    return TestCase(**metadata).model_dump(exclude_none=True)

def _extract_test_name(code: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Gets the test suite and case names from the TEST macro.
    """
    m = re.match(r"(TEST|TEST_F)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", code)
    if m:
        testsuite_name = m.group(2)
        testcase_name = m.group(3)
    return testsuite_name, testcase_name

def discover_testcases(code: str) -> List[TestCase]:
    testcases = list[TestCase]()
    for row, line in enumerate(code):
        if line.startswith("TEST"):
            suite_name, case_name = _extract_test_name(code[row])
            if suite_name and case_name:
                metadata = _extract_testcase_metadata(code, row)
                metadata["id"] = f"{suite_name}.{case_name}"
                testcases.append(metadata)
    return testcases

def discover_testsuite(code: str) -> TestSuite:
    """
    Scans the first lines of the file for testsuite metadata.
    """
    row = 0
    metadata = {}
    while code[row].startswith("//@"):
        key, value = _extract_metadata(code[row])
        if key:
            metadata[key] = value
        row += 1
    return TestSuite(**metadata)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: discover_tests.py <test_file> [output_file]", file=sys.stderr)
        sys.exit(1)

    test_file = sys.argv[1]
    code = Path(test_file).read_text().splitlines()
    suite = discover_testsuite(code)
    tests = discover_testcases(code)
    suite.tests = TypeAdapter(List[TestCase]).validate_python(tests)
    output = suite.model_dump_json(exclude_none=True)

    # Write JSON to output file if provided.
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        with open(output_file, "w") as f:
            f.write(output)

    print(output)