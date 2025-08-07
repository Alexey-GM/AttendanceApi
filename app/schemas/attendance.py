from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class AttendanceStatusResponse(BaseModel):
    id: int
    name: str
    comment: Optional[str] = None

    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_birth: Optional[str] = None
    base_group_id: int

    class Config:
        from_attributes = True

class ClassroomResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AttendanceResponse(BaseModel):
    id: int
    student: StudentResponse
    attendance_status: AttendanceStatusResponse
    attendance_timestamp: str
    comment: Optional[str] = None

    class Config:
        from_attributes = True

class AttendanceSessionResponse(BaseModel):
    id: int
    date: str
    classroom: ClassroomResponse
    attendances: List[AttendanceResponse] = []

    class Config:
        from_attributes = True

# Схемы для создания
class CreateAttendanceSessionRequest(BaseModel):
    discipline_plan_id: int
    date: date
    classroom_id: int 