import json
import re
import sys

from pathlib import Path
from pydantic import BaseModel, field_validator
from typing import Optional

class TestMetadata(BaseModel):
    name: Optional[str] = None
    hidden: Optional[bool] = None
    private: Optional[bool] = None
    score: Optional[float] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    ok: Optional[bool] = None
    passed: Optional[bool] = None
    feedback: Optional[str] = None
    expected: Optional[str] = None
    observed: Optional[str] = None
    expand_feedback: Optional[bool] = None

    @field_validator("feedback", "expected", "observed", mode="before")
    def fix_str_field(cls, v):
        if isinstance(v, bool):
            return ""
        return v

    @field_validator("feedback", "expected", "observed", mode="before")
    def unicode_escape(cls, v):
        if isinstance(v, str):
            return v.encode("utf-8").decode("unicode_escape")
        return v

def extract_test_metadata(code: list[str], row: int) -> dict:
    """
    Scans previous lines from the given line for testcase metadata.
    """
    row -= 1
    metadata = {}
    while row >= 0 and code[row].startswith("//@"):
        m = re.match(r"\/\/@(\w+)\s*(.*)", code[row])
        if m:
            key = m.group(1)
            value = m.group(2) or True
            metadata[key] = value
        row -= 1
    return TestMetadata(**metadata).model_dump(exclude_none=True)

def extract_test_name(code: str) -> tuple:
    """
    Gets the test suite and case names from the TEST macro.
    """
    m = re.match(r"(TEST|TEST_F)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", code)
    if m:
        testsuite_name = m.group(2)
        testcase_name = m.group(3)
        return testsuite_name, testcase_name
    return None, None

def discover_testcases(test_file: str) -> list[dict]:
    code = Path(test_file).read_text().splitlines()
    testcases = []
    for row, line in enumerate(code):
        if line.startswith("TEST"):
            args = extract_test_name(code[row])
            metadata = extract_test_metadata(code, row)
            testcases.append({
                "id": args[0] + "." + args[1],
                **metadata,
            })
    return testcases

if __name__ == "__main__":
    test_file = sys.argv[1]
    output_file = sys.argv[2]
    tests = discover_testcases(test_file)
    with open(output_file, "w+") as f:
        json.dump(tests, f)
        print(tests)