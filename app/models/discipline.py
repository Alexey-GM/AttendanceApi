from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class Discipline(Base):
    __tablename__ = "discipline"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 