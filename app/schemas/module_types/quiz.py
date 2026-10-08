from pydantic import BaseModel, Field, model_validator


class QuizQuestion(BaseModel):
    text: str
    options: list[str] = Field(min_length=2)
    correct: list[int] = Field(min_length=1)  # indexes into options

    @model_validator(mode="after")
    def _check_indexes(self) -> "QuizQuestion":
        if any(not 0 <= i < len(self.options) for i in self.correct):
            raise ValueError("correct index out of range")
        return self


class QuizContent(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=1)
    pass_score: float = 70.0


class QuizSubmission(BaseModel):
    answers: list[list[int]]  # selected option indexes per question
