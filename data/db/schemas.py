from pydantic import BaseModel
from typing import Optional

class SubjectBase(BaseModel):
    name: str
    lecturer: Optional[str] = None
    hours: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True
