from sqlalchemy.orm import Session
from data.models.user import User
from passlib.hash import bcrypt
from sqlalchemy.exc import SQLAlchemyError

def get_user_by_login(db: Session, login: str):
    try:
        user = db.query(User).filter(User.login == login).first()
        if not user:
            raise ValueError(f"User with login {login} not found")
        return user
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching user: {str(e)}")

def get_all_teachers(db: Session):
    try:
        return db.query(User).filter(User.role == "teacher").all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching teachers: {str(e)}")

def create_user(db: Session, user_data: dict):
    try:
        if not all(key in user_data for key in ["first_name", "last_name", "login", "password"]):
            raise ValueError("Missing required fields")
            
        user_data["password"] = bcrypt.hash(user_data["password"])
        user_data["role"] = user_data.get("role", "student")
        
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating user: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def update_password(db: Session, user_id: int, old_password: str, new_password: str):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        if not bcrypt.verify(old_password, user.password):
            raise ValueError("Old password is incorrect")
        
        user.password = bcrypt.hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating password: {str(e)}")

def update_user_fio(db: Session, user_id: int, fio_data: dict):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        for field in ["first_name", "last_name", "patronymic"]:
            if field in fio_data:
                setattr(user, field, fio_data[field])
        
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating user info: {str(e)}")
