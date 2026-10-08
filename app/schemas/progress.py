from pydantic import BaseModel, ConfigDict


class ProgressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    module_id: int
    score: float
    completed: bool
    attempts: int


class SubjectProgress(BaseModel):
    subject_id: int
    total_modules: int
    completed_modules: int
    percent: float
