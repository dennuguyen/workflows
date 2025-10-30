import json
import sys

from pydantic import BaseModel
from typing import Optional, List

class Report(BaseModel):
    """
    Fields expected by @classroom-resources/autograding-grading-reporter GitHub Action.
    """
    name: str
    status: str
    message: Optional[str] = None
    line_no: Optional[int] = None
    test_code: Optional[int] = None

class FinalReport(BaseModel):
    tests: List[Report]
    max_score: int

def report_tests(results: str):
    reports: List[Report] = []
    total_max = 0

    for result in results:
        name = result.get("name") or result.get("id")

        if not result.get("ok", True):
            status = "error"
        elif result.get("passed"):
            status = "passed"
        else:
            status = "failed"

        message_parts = []
        if "feedback" in result and result.get("feedback"):
            message_parts.append(str(result.get("feedback")))
        if "expected" in result and result.get("expected") is not None:
            message_parts.append(f"Expected: {result.get('expected')}")
        if "observed" in result and result.get("observed") is not None:
            message_parts.append(f"Observed: {result.get('observed')}")

        message = "\n".join(message_parts) if message_parts else None

        score_val = 0
        if "score" in result and result.get("score") is not None:
            try:
                score_val = int(round(float(result.get("score"))))
            except Exception:
                score_val = 0

        total_max += score_val

        reports.append(Report(name=name, status=status, message=message))

    final = FinalReport(tests=reports, max_score=total_max)
    return final.model_dump(exclude_none=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: report_tests.py <result_file> [output_file]", file=sys.stderr)
        sys.exit(1)
    
    result_file = sys.argv[1]

    results = json.load(open(result_file, "r"))
    report = report_tests(results)

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        with open(output_file, "w") as f:
            f.write(report)

    print(report)