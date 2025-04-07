from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects
from routers import student_group
from routers import lecturer
from routers import schedule
from routers import students
from routers import attendances

app = FastAPI()

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(student_group.router)
app.include_router(lecturer.router)
app.include_router(subjects.router)
app.include_router(schedule.router)
app.include_router(students.router)
app.include_router(attendances.router)