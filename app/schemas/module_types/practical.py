from pydantic import BaseModel, Field


class PracticalStep(BaseModel):
    text: str
    required: bool = True


class PracticalContent(BaseModel):
    instructions: str
    steps: list[PracticalStep] = Field(min_length=1)


class PracticalSubmission(BaseModel):
    completed_steps: list[int]  # indexes of finished steps
    report: str = ""
