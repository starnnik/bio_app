from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Module, Progress
from app.modules.base import Evaluation
from app.schemas.progress import SubjectProgress


async def record_attempt(session: AsyncSession, user_id: int, module_id: int, result: Evaluation) -> Progress:
    progress = await session.scalar(
        select(Progress).where(Progress.user_id == user_id, Progress.module_id == module_id)
    )
    if progress is None:
        progress = Progress(user_id=user_id, module_id=module_id, attempts=0, score=0.0, completed=False)
        session.add(progress)
    progress.attempts += 1
    progress.score = max(progress.score, result.score)
    progress.completed = progress.completed or result.passed
    await session.commit()
    return progress


async def list_progress(session: AsyncSession, user_id: int) -> list[Progress]:
    rows = await session.scalars(select(Progress).where(Progress.user_id == user_id))
    return list(rows)


async def subject_progress(session: AsyncSession, user_id: int, subject_id: int) -> SubjectProgress:
    total = await session.scalar(select(func.count()).select_from(Module).where(Module.subject_id == subject_id))
    done = await session.scalar(
        select(func.count())
        .select_from(Progress)
        .join(Module, Module.id == Progress.module_id)
        .where(Progress.user_id == user_id, Module.subject_id == subject_id, Progress.completed)
    )
    total, done = total or 0, done or 0
    return SubjectProgress(
        subject_id=subject_id,
        total_modules=total,
        completed_modules=done,
        percent=round(100 * done / total, 1) if total else 0.0,
    )
