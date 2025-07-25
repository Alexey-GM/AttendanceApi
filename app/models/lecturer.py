from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Lecturer(Base):
    __tablename__ = "lecturer"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    login = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False) 