from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects
from routers import student_group
from routers import user
from routers import schedule
from routers import students
from routers import attendances

from fastapi.exceptions import HTTPException
from fastapi import Request
from data.response import format_response

app = FastAPI()

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