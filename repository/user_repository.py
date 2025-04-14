from sqlalchemy.orm import Session
from data.models.user import User
from passlib.hash import bcrypt

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def get_all_teachers(db: Session):
    return db.query(User).filter(User.role == "teacher").all()

def create_user(db: Session, user_data: dict):
    user_data["password"] = bcrypt.hash(user_data["password"])
    user_data["role"] = "student"  # Default role for new users
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_password(db: Session, user_id: int, old_password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user and bcrypt.verify(old_password, user.password):
        user.password = bcrypt.hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    return None

def update_user_fio(db: Session, user_id: int, fio_data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for field in ["first_name", "last_name", "patronymic"]:
        if field in fio_data:
            setattr(user, field, fio_data[field])
    db.commit()
    db.refresh(user)
    return user
