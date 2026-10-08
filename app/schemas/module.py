from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.module import ModuleType


class ModuleCreate(BaseModel):
    subject_id: int
    type: ModuleType
    title: str
    position: int = 0
    content: dict[str, Any]


class ModuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    type: ModuleType
    title: str
    position: int
    content: dict[str, Any]


class SubmissionResult(BaseModel):
    score: float
    passed: bool
    feedback: str = ""
