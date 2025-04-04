from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects
from routers import student_group

app = FastAPI()

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(subjects.router)
app.include_router(student_group.router)