from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class Classroom(Base):
    __tablename__ = "classroom"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 