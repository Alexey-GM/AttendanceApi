# AttendanceApi

## Структура проекта

```
AttendanceApi/
├── app/
│   ├── main.py
│   ├── core/
│   ├── api/
│   │   ├── auth/
│   │   ├── attendance/
│   │   ├── students/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── db/
│   ├── utils/
│   └── middleware/
├── alembic/
├── tests/
├── .env
├── requirements.txt
```

## Быстрый старт (Windows)

1. Установите зависимости:
   ```
pip install -r requirements.txt
   ```
2. Запустите сервер:
   ```
uvicorn app.main:app --reload
   ```

## Реализовано
- Регистрация и вход пользователя (заглушки, без БД)
- Единообразные ответы API

## Дальнейшие шаги
- Реализация моделей, подключения к БД, JWT-проверки, остальных роутов 

## Схема БД (фрагмент для аутентификации)

- lecturer(id, first_name, last_name, middle_name, login, password, department_id)
- department(id, short_name, full_name, faculty_id)
- faculty(id, short_name, full_name)

## Пример строки подключения

В файле `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/attendance_db
``` 