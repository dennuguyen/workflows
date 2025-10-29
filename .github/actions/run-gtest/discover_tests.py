import re
import sys

from clang.cindex import CursorKind, Index, TranslationUnit
from pathlib import Path
from pydantic import BaseModel, field_validator
from typing import Optional

def discover_testcases(test_file: str) -> list[dict]:
    index = Index.create()
    tu = index.parse(test_file, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
    code = Path(test_file).read_text().splitlines()
    testcases = []

    # Traverse the AST.
    for cursor in tu.cursor.walk_preorder():
        try:
            if cursor.kind == CursorKind.MACRO_INSTANTIATION and cursor.spelling.startswith("TEST"):
                line = cursor.location.line
                args = extract_test_macro_args(code[line - 1]) # -1 to account for 0 index.
                metadata = extract_test_metadata(code, line)
                testcases.append({
                    "test_file": test_file,
                    "test_runner": "./" + Path(test_file).stem + ".out",
                    "id": args[0] + "." + args[1],
                    **metadata,
                })
        except ValueError as e:
            continue
    return testcases

def extract_test_macro_args(code: str) -> tuple:
    """
    Gets the test suite and case names from the TEST macro.
    """
    m = re.match(r"(TEST|TEST_F)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", code)
    if m:
        testsuite_name = m.group(2)
        testcase_name = m.group(3)
        return testsuite_name, testcase_name
    return None, None

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

def extract_test_metadata(code: list[str], line: int) -> dict:
    """
    Scans previous lines from the given line for testcase metadata.
    """
    line -= 1
    metadata = {}
    while line >= 0 and code[line - 1].startswith("//@"):
        m = re.match(r"\/\/@(\w+)\s*(.*)", code[line - 1])
        if m:
            key = m.group(1)
            value = m.group(2) or True
            metadata[key] = value
        line -= 1
    return TestMetadata(**metadata).model_dump(exclude_none=True)

discover_testcases(sys.argv[0])