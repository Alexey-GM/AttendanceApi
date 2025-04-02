from fastapi import FastAPI
from data.db.db import engine, Base
from routers import subjects

app = FastAPI()

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(subjects.router)