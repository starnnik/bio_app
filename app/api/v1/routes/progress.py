from fastapi import APIRouter

from app.api.v1.dependencies import CurrentUser, SessionDep
from app.models import Progress
from app.schemas.progress import ProgressRead, SubjectProgress
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[ProgressRead])
async def my_progress(user: CurrentUser, session: SessionDep) -> list[Progress]:
    return await progress_service.list_progress(session, user.id)


@router.get("/subjects/{subject_id}", response_model=SubjectProgress)
async def my_subject_progress(subject_id: int, user: CurrentUser, session: SessionDep) -> SubjectProgress:
    return await progress_service.subject_progress(session, user.id, subject_id)
