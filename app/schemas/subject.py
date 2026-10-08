from pydantic import BaseModel, ConfigDict


class SubjectCreate(BaseModel):
    title: str
    description: str = ""


class SubjectRead(SubjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
