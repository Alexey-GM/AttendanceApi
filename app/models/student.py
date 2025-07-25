from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.models.lecturer import Base

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    date_birth = Column(Date, nullable=False)
    base_group_id = Column(Integer, ForeignKey("base_group.id"), nullable=False) 