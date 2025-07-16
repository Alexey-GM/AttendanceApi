from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects
from routers import student_group
from routers import user
from routers import schedule
from routers import students
from routers import attendances

from routers import risk_students
from routers import direction_attendance
from routers import attendance_chart_routers
from routers import attendance_groups_routers
from routers import attendance_weekly_service
from routers import student_attendance_router
from routers import attendance_student_subject

from fastapi.exceptions import HTTPException
from fastapi import Request
from data.response import format_response
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

app = FastAPI()

class Settings(BaseSettings):
    FRONT: str

    class Config:
        env_file = ".env" 

        extra = "allow"  

settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы
Base.metadata.create_all(bind=engine)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return format_response(message="Internal Server Error", code=500)


# Подключаем маршруты
app.include_router(student_group.router)
app.include_router(user.router)
app.include_router(subjects.router)
app.include_router(schedule.router)
app.include_router(students.router)
app.include_router(attendances.router)

#Для фронта

app.include_router(risk_students.router)
app.include_router(direction_attendance.router)
app.include_router(attendance_chart_routers.router)
app.include_router(attendance_groups_routers.router)
app.include_router(attendance_weekly_service.router)
app.include_router(student_attendance_router.router)
app.include_router(attendance_student_subject.router)