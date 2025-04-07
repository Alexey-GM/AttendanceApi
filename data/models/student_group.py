from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.db.db import Base

class StudentGroup(Base):
    __tablename__ = "student_group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    direction = Column(String(100))
    course = Column(Integer)

    schedules = relationship("Schedule", back_populates="group_relation") 
    students = relationship("Student", back_populates="group_relation") 
