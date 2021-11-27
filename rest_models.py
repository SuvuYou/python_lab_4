from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, fields

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:11111111@localhost:3306/online_courses_lab'
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'

    student_id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column('first_name', db.String(32))
    last_name=db.Column('last_name', db.String(32))
    email=db.Column('email', db.String(32))
    password=db.Column('password', db.String(32))
    iq=db.Column("iq", db.Integer)
    GPA=db.Column('GPA', db.Integer)

    join_requests = db.relationship('Join_Request', backref='student', lazy=True)

rf_student = {
    "student_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "iq": fields.Integer,
    "GPA": fields.Integer,
}    

args_student = reqparse.RequestParser()
args_student.add_argument("first_name", type=str, help="first_name is required", required=True)
args_student.add_argument("last_name", type=str, help="last_name is required", required=True)
args_student.add_argument("email", type=str, help="email is required", required=True)
args_student.add_argument("password", type=str, help="password is required", required=True)
args_student.add_argument("iq", type=int, help="iq is required", required=True)
args_student.add_argument("GPA", type=int, help="GPA is required", required=True)

args_student_update = reqparse.RequestParser()
args_student_update.add_argument("first_name", type=str)
args_student_update.add_argument("last_name", type=str)
args_student_update.add_argument("email", type=str)
args_student_update.add_argument("password", type=str)
args_student_update.add_argument("iq", type=int)
args_student_update.add_argument("GPA", type=int)

class Professor(db.Model):
    __tablename__ = 'professor'

    professor_id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column('first_name', db.String(32))
    last_name=db.Column('last_name', db.String(32))
    email=db.Column('email', db.String(32))
    password=db.Column('password', db.String(32))
    subject=db.Column("subject", db.String(32))

    courses = db.relationship('Course', backref='professor', lazy=True)

rf_professor = {
    "professor_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "subject": fields.String,
}   

args_professor = reqparse.RequestParser()
args_professor.add_argument("first_name", type=str, help="first_name is required", required=True)
args_professor.add_argument("last_name", type=str, help="last_name is required", required=True)
args_professor.add_argument("email", type=str, help="email is required", required=True)
args_professor.add_argument("password", type=str, help="password is required", required=True)
args_professor.add_argument("subject", type=str, help="subject is required", required=True)

args_professor_update = reqparse.RequestParser()
args_professor_update.add_argument("first_name", type=str)
args_professor_update.add_argument("last_name", type=str)
args_professor_update.add_argument("email", type=str)
args_professor_update.add_argument("password", type=str)
args_professor_update.add_argument("subject", type=str)

class Course(db.Model):
    __tablename__ = 'course'

    course_id=db.Column(db.Integer, primary_key=True)
    professor_id=db.Column(db.Integer, db.ForeignKey('professor.professor_id'))
    subject=db.Column('subject', db.String(32))

rf_course = {
    "course_id": fields.Integer,
    "professor_id": fields.Integer,
    "subject": fields.String,
}   

args_course = reqparse.RequestParser()
args_course.add_argument("professor_id", type=int, help="professor_id is required", required=True)
args_course.add_argument("subject", type=str, help="last_name is required", required=True)

args_course_update = reqparse.RequestParser()
args_course_update.add_argument("professor_id", type=int)
args_course_update.add_argument("subject", type=str)

class Join_Request(db.Model):
    __tablename__ = 'join_request'

    join_request_id=db.Column(db.Integer, primary_key=True)
    course_id=db.Column(db.Integer, db.ForeignKey('course.course_id'))
    student_id=db.Column(db.Integer, db.ForeignKey('student.student_id'))
    status=db.Column('status', db.String(32))

rf_join_request = {
    "join_request_id": fields.Integer,
    "course_id": fields.Integer,
    "student_id": fields.Integer,
    "status": fields.String,
}   

args_join_request = reqparse.RequestParser()
args_join_request.add_argument("course_id", type=int, help="course_id is required", required=True)
args_join_request.add_argument("student_id", type=int, help="student_id is required", required=True)
args_join_request.add_argument("status", type=str, help="status is required", required=True)

args_join_request_update = reqparse.RequestParser()
args_join_request_update.add_argument("course_id", type=int)
args_join_request_update.add_argument("student_id", type=int)
args_join_request_update.add_argument("status", type=str)

class Course_Student(db.Model):
    __tablename__ = 'course_student'

    course_student_id=db.Column(db.Integer, primary_key=True)
    course_id=db.Column(db.Integer, db.ForeignKey('course.course_id'))
    student_id=db.Column(db.Integer, db.ForeignKey('student.student_id'))

    courses = db.relationship('Course', backref='course_student', lazy=True)
    students = db.relationship('Student', backref='course_student', lazy=True)

rf_course_student = {
    "course_id": fields.Integer,
    "student_id": fields.Integer,
}   

args_course_student = reqparse.RequestParser()
args_course_student.add_argument("course_id", type=int, help="course_id is required", required=True)
args_course_student.add_argument("student_id", type=int, help="student_id is required", required=True)