from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from data.db.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50)) 
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) 

    subjects = relationship("Subject", back_populates="teacher_relation")