from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar

from pydantic import BaseModel


@dataclass
class Evaluation:
    score: float  # 0..100
    passed: bool
    feedback: str = ""


class BaseModule(ABC):
    """Behaviour of one module type. Subclasses are stateless and registered by type."""

    content_schema: ClassVar[type[BaseModel]]
    submission_schema: ClassVar[type[BaseModel]]

    def validate_content(self, content: dict[str, Any]) -> dict[str, Any]:
        return self.content_schema.model_validate(content).model_dump()

    def public_content(self, content: dict[str, Any]) -> dict[str, Any]:
        """Content shown to learners (hide answers here)."""
        return content

    def parse_submission(self, data: dict[str, Any]) -> BaseModel:
        return self.submission_schema.model_validate(data)

    @abstractmethod
    def evaluate(self, content: dict[str, Any], submission: BaseModel) -> Evaluation: ...
