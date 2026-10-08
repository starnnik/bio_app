from pydantic import BaseModel


class TheoreticalContent(BaseModel):
    body: str  # markdown text


class TheoreticalSubmission(BaseModel):
    pass  # reading is confirmed by submitting an empty payload
