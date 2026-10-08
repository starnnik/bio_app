from typing import Any

from pydantic import BaseModel

from app.modules.base import BaseModule, Evaluation
from app.schemas.module_types.practical import PracticalContent, PracticalSubmission


class PracticalModule(BaseModule):
    """Self-reported checklist; the score is the share of finished steps."""

    content_schema = PracticalContent
    submission_schema = PracticalSubmission

    def evaluate(self, content: dict[str, Any], submission: BaseModel) -> Evaluation:
        task = PracticalContent.model_validate(content)
        done = set(PracticalSubmission.model_validate(submission).completed_steps)
        required = {i for i, s in enumerate(task.steps) if s.required}
        score = round(100 * len(done & set(range(len(task.steps)))) / len(task.steps), 1)
        missing = sorted(required - done)
        return Evaluation(score, not missing, f"missing required steps: {missing}" if missing else "")
