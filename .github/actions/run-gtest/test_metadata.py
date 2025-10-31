from pydantic import BaseModel, field_validator
from typing import Optional

class TestMetadata(BaseModel):
    name: Optional[str] = None
    hidden: Optional[bool] = None
    secret: Optional[bool] = None
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