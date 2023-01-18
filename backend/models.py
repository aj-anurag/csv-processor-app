from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    age = Column(Integer)
    grade = Column(String(50))



