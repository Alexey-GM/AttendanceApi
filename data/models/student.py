from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from data.db.db import Base  

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    date_birth = Column(Date, nullable=True)
    group_id = Column(Integer, ForeignKey('student_group.id'))

    group_relation = relationship("StudentGroup", back_populates="students") 
    attendances = relationship("Attendance", back_populates="student_relation")