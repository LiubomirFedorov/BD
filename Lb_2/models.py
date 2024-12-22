from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    courses = relationship("Course", back_populates="category")

class Instructor(Base):
    __tablename__ = 'instructors'

    instructor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    bio = Column(Text)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")

    courses = relationship("Course", back_populates="instructor")


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    category_id = Column(ForeignKey('categories.category_id'))
    instructor_id = Column(ForeignKey('instructors.instructor_id'))
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    
    category = relationship("Category", back_populates="courses")
    instructor = relationship("Instructor", back_populates="courses")

    enrollments = relationship("Enrollment", back_populates="course")

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    registration_date = Column(Date)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default=None, nullable=True) 

    enrollments = relationship("Enrollment", back_populates="student")


class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(ForeignKey('students.student_id'))
    course_id = Column(ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    progress_percentage = Column(Integer, default=0)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
