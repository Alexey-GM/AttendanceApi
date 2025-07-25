from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.lecturer import Lecturer
from passlib.hash import bcrypt
from app.schemas.auth import UserCreate, UserLogin
from app.utils.jwt import create_access_token
from datetime import timedelta

async def register_user(user: UserCreate, db: AsyncSession) -> dict:
    hashed_password = bcrypt.hash(user.password)
    lecturer = Lecturer(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        department_id=user.department_id,
    )
    db.add(lecturer)
    try:
        await db.commit()
        await db.refresh(lecturer)
    except IntegrityError as e:
        await db.rollback()
        raise Exception(str(e.orig))
    return {"login": lecturer.login, "first_name": lecturer.first_name, "last_name": lecturer.last_name}

async def login_user(user: UserLogin, db: AsyncSession) -> dict:
    q = await db.execute(select(Lecturer).where(Lecturer.login == user.login))
    lecturer = q.scalar_one_or_none()
    if not lecturer or not bcrypt.verify(user.password, lecturer.password):
        raise Exception("Invalid login or password")
    access_token = create_access_token({"sub": str(lecturer.id)}, expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"} 