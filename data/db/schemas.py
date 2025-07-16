from pydantic import BaseModel
from typing import Optional, List

class SubjectBase(BaseModel):
    name: str
    teacher_id: Optional[int] = None
    hours: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True

class StudentGroupResponse(BaseModel):
    id: int
    name: str
    direction: Optional[str] = None
    course: Optional[int] = None

    class Config:
        from_attributes = True

class ScheduleWithDetailsResponse(BaseModel):
    id: int
    subject: SubjectResponse
    group: StudentGroupResponse
    date: str
    classroom: Optional[str] = None
    type_class: Optional[str] = None
    start_time: str
    end_time: str

    class Config:
        from_attributes = True

class ScheduleShortResponse(BaseModel):
    id: int
    group: StudentGroupResponse
    date: str
    classroom: Optional[str] = None
    type_class: Optional[str] = None
    start_time: str
    end_time: str

    class Config:
        from_attributes = True

class ScheduleWrapperResponse(BaseModel):
    subject: SubjectResponse
    schedule: List[ScheduleShortResponse]
