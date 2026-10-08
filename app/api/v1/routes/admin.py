from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.api.v1.dependencies import SessionDep, require_admin
from app.models import Module, Subject
from app.schemas.module import ModuleCreate, ModuleRead
from app.schemas.subject import SubjectCreate, SubjectRead
from app.services import module_executor

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/subjects", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
async def create_subject(data: SubjectCreate, session: SessionDep) -> Subject:
    subject = Subject(**data.model_dump())
    session.add(subject)
    await session.commit()
    return subject


@router.delete("/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: int, session: SessionDep) -> None:
    subject = await session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(404, "Subject not found")
    await session.delete(subject)
    await session.commit()


@router.post("/modules", response_model=ModuleRead, status_code=status.HTTP_201_CREATED)
async def create_module(data: ModuleCreate, session: SessionDep) -> Module:
    if await session.get(Subject, data.subject_id) is None:
        raise HTTPException(404, "Subject not found")
    try:
        content = module_executor.validate_content(data.type, data.content)
    except ValidationError as exc:
        raise HTTPException(422, exc.errors(include_url=False, include_context=False)) from exc
    module = Module(**{**data.model_dump(), "content": content})
    session.add(module)
    await session.commit()
    return module


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(module_id: int, session: SessionDep) -> None:
    module = await session.get(Module, module_id)
    if module is None:
        raise HTTPException(404, "Module not found")
    await session.delete(module)
    await session.commit()
