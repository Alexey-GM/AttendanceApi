from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from data.db.db import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    schedule = Column(Integer, ForeignKey('schedule.id'), nullable=False)
    student = Column(Integer, ForeignKey('student.id'), nullable=False)
    status = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    schedule_relation = relationship("Schedule", back_populates="attendances")
    student_relation = relationship("Student", back_populates="attendances")
