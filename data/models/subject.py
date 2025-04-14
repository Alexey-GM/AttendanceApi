from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.db.db import Base

class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'))  
    hours = Column(Integer)

    teacher_relation = relationship("User", back_populates="subjects")
    schedules = relationship("Schedule", back_populates="subject_relation")