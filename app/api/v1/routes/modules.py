from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import select

from app.api.v1.dependencies import CurrentUser, SessionDep
from app.models import Module
from app.schemas.module import ModuleRead, SubmissionResult
from app.services import module_executor, progress_service

router = APIRouter(prefix="/modules", tags=["modules"])


def _to_read(module: Module) -> ModuleRead:
    return ModuleRead(
        id=module.id,
        subject_id=module.subject_id,
        type=module.type,
        title=module.title,
        position=module.position,
        content=module_executor.public_content(module),
    )


async def _get_or_404(session: SessionDep, module_id: int) -> Module:
    module = await session.get(Module, module_id)
    if module is None:
        raise HTTPException(404, "Module not found")
    return module


@router.get("", response_model=list[ModuleRead])
async def list_modules(_: CurrentUser, session: SessionDep, subject_id: int) -> list[ModuleRead]:
    rows = await session.scalars(
        select(Module).where(Module.subject_id == subject_id).order_by(Module.position, Module.id)
    )
    return [_to_read(m) for m in rows]


@router.get("/{module_id}", response_model=ModuleRead)
async def get_module(module_id: int, _: CurrentUser, session: SessionDep) -> ModuleRead:
    return _to_read(await _get_or_404(session, module_id))


@router.post("/{module_id}/submit", response_model=SubmissionResult)
async def submit(module_id: int, payload: dict[str, Any], user: CurrentUser, session: SessionDep) -> SubmissionResult:
    module = await _get_or_404(session, module_id)
    try:
        result = module_executor.execute(module, payload)
    except (ValidationError, ValueError) as exc:
        raise HTTPException(422, str(exc)) from exc
    await progress_service.record_attempt(session, user.id, module.id, result)
    return SubmissionResult(score=result.score, passed=result.passed, feedback=result.feedback)
