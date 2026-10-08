from typing import Any

from pydantic import BaseModel

from app.modules.base import BaseModule, Evaluation
from app.schemas.module_types.theoretical import TheoreticalContent, TheoreticalSubmission


class TheoreticalModule(BaseModule):
    content_schema = TheoreticalContent
    submission_schema = TheoreticalSubmission

    def evaluate(self, content: dict[str, Any], submission: BaseModel) -> Evaluation:
        return Evaluation(score=100.0, passed=True)
