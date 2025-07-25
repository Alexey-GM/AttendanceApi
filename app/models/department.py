from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from app.models.lecturer import Base

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False) 