from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class Specialty(Base):
    __tablename__ = "specialty"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    code = Column(String, nullable=False)