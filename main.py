from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects
from routers import student_group
from routers import lecturer

app = FastAPI()

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(student_group.router)
app.include_router(lecturer.router)
app.include_router(subjects.router)