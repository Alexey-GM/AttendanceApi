from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from data.db.db import Base

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    student_subject = Column(Integer, ForeignKey('subject.id'), nullable=False)  
    group_id = Column(Integer, ForeignKey('student_group.id'), nullable=False)    
    date = Column(Date, nullable=False)
    classroom = Column(String(50), nullable=True)
    type_class = Column(String(20), nullable=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    subject_relation = relationship("Subject", back_populates="schedules")
    group_relation = relationship("StudentGroup", back_populates="schedules")
    attendances = relationship("Attendance", back_populates="schedule_relation")
