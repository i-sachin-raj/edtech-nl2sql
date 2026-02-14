from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime,timezone
from .database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    grade = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.now(timezone.utc))
