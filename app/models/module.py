import enum
from typing import Any

from sqlalchemy import JSON, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.subject import Subject


class ModuleType(enum.StrEnum):
    THEORETICAL = "theoretical"
    QUIZ = "quiz"
    PRACTICAL = "practical"


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), index=True)
    type: Mapped[ModuleType] = mapped_column(Enum(ModuleType))
    title: Mapped[str] = mapped_column(String(255))
    position: Mapped[int] = mapped_column(default=0)
    # Type-specific payload, validated by the matching schema in app/schemas/module_types.
    content: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    subject: Mapped[Subject] = relationship(back_populates="modules")
