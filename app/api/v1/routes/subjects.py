from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.v1.dependencies import CurrentUser, SessionDep
from app.models import Subject
from app.schemas.subject import SubjectRead

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("", response_model=list[SubjectRead])
async def list_subjects(_: CurrentUser, session: SessionDep) -> list[Subject]:
    return list(await session.scalars(select(Subject).order_by(Subject.id)))


@router.get("/{subject_id}", response_model=SubjectRead)
async def get_subject(subject_id: int, _: CurrentUser, session: SessionDep) -> Subject:
    subject = await session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(404, "Subject not found")
    return subject
