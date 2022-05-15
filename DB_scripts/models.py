from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'

    student_id=Column(Integer, primary_key=True)
    first_name=Column('first_name', String(32))
    last_name=Column('last_name', String(32))
    email=Column('email', String(32))
    password=Column('password', String(32))
    Iq=Column("iq", Integer)
    Gpa=Column('GPA', Integer)

class Professor(Base):
    __tablename__ = 'professor'

    professor_id=Column(Integer, primary_key=True)
    first_name=Column('first_name', String(32))
    last_name=Column('last_name', String(32))
    email=Column('email', String(32))
    password=Column('password', String(32))
    subject=Column('subject', String(32))

class Course(Base):
    __tablename__ = 'course'

    course_id=Column(Integer, primary_key=True)
    professor_id=Column(Integer, ForeignKey('professor.professor_id'))
    subject=Column('subject', String(32))

    professor = relationship("Professor")


class Course_student(Base):
    __tablename__ = 'course_student'

    course_student_id=Column(Integer, primary_key=True)
    course_id=Column(Integer, ForeignKey('course.course_id'))
    student_id=Column(Integer, ForeignKey('student.student_id'))

    course = relationship("Course")
    student = relationship("Student")

class Join_request(Base):
    __tablename__ = 'join_request'

    join_request_id=Column(Integer, primary_key=True)
    course_id=Column(Integer, ForeignKey('course.course_id'))
    student_id=Column(Integer, ForeignKey('student.student_id'))
    status=Column('status', String(32))   

    course = relationship("Course")
    student = relationship("Student")
