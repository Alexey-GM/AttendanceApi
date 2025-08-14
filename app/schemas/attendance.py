from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict

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

# Схемы для статистики посещаемости по курсам
class CourseAttendanceStats(BaseModel):
    course: str
    attendance: float

class PeriodAttendanceStats(BaseModel):
    period: str
    courses: List[CourseAttendanceStats]

class CourseAttendanceResponse(BaseModel):
    periods: Dict[str, List[CourseAttendanceStats]] 

# Схемы для статистики посещаемости по направлениям
class DirectionAttendanceStats(BaseModel):
    direction: str
    attendance: float

class DirectionAttendanceResponse(BaseModel):
    periods: Dict[str, List[DirectionAttendanceStats]] 

# Схемы для студентов в зоне риска
class StudentRiskStats(BaseModel):
    name: str
    group: str
    missed: int

class StudentsRiskResponse(BaseModel):
    students: List[StudentRiskStats]

# Схемы для посещаемости по группам
class GroupAttendanceData(BaseModel):
    date: str
    # Динамические поля для групп будут добавляться автоматически

class GroupAttendanceWeek(BaseModel):
    week: str
    data: List[GroupAttendanceData]
    trend: Dict[str, str]

class GroupAttendanceResponse(BaseModel):
    weeks: List[GroupAttendanceWeek]

# Схемы для посещаемости за 4 недели
class WeekGroupAttendance(BaseModel):
    group: str
    direction: str
    course: str
    attendancePercent: float

class WeekAttendanceData(BaseModel):
    weekStart: str
    weekEnd: str
    isoWeek: int
    even: bool
    data: List[WeekGroupAttendance]

class FourWeeksAttendanceResponse(BaseModel):
    weeks: List[WeekAttendanceData] 

# Схемы для посещаемости студента за 4 недели
class StudentWeekAttendance(BaseModel):
    weekType: str
    start: str
    end: str
    isoWeek: int
    attendancePercent: float

class StudentAttendancePeriod(BaseModel):
    startDate: str
    endDate: str

class StudentAttendanceData(BaseModel):
    student: str
    subject: str
    lessonType: str
    period: StudentAttendancePeriod
    weeks: List[StudentWeekAttendance]

class StudentAttendanceResponse(BaseModel):
    data: List[StudentAttendanceData] 

# Схемы для общей посещаемости студента
class StudentAttendanceRecord(BaseModel):
    fullName: str
    group: str
    course: int
    subject: str
    teacher: str
    date: str
    status: int
    comment: str

class GeneralStudentAttendanceResponse(BaseModel):
    data: List[StudentAttendanceRecord] 