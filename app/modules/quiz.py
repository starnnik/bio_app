from typing import Any

from pydantic import BaseModel

from app.modules.base import BaseModule, Evaluation
from app.schemas.module_types.quiz import QuizContent, QuizSubmission


class QuizModule(BaseModule):
    content_schema = QuizContent
    submission_schema = QuizSubmission

    def public_content(self, content: dict[str, Any]) -> dict[str, Any]:
        return {
            **content,
            "questions": [{k: v for k, v in q.items() if k != "correct"} for q in content["questions"]],
        }

    def evaluate(self, content: dict[str, Any], submission: BaseModel) -> Evaluation:
        quiz = QuizContent.model_validate(content)
        answers = QuizSubmission.model_validate(submission).answers
        if len(answers) != len(quiz.questions):
            raise ValueError("answers must match the number of questions")
        right = sum(set(a) == set(q.correct) for q, a in zip(quiz.questions, answers, strict=True))
        score = round(100 * right / len(quiz.questions), 1)
        return Evaluation(score, score >= quiz.pass_score, f"{right}/{len(quiz.questions)} correct")
