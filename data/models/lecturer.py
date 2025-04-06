from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from data.db.db import Base

class Lecturer(Base):
    __tablename__ = "lecturer"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    middle_name = Column(String(50))
    date_birth = Column(Date)
    phone = Column(String(20))

    subjects = relationship("Subject", back_populates="lecturer_relation")