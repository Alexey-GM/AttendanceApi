from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False) 