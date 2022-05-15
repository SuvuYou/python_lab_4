# from create_tables import engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Course, Professor, Course_student, Join_request

engine = create_engine('mysql+pymysql://root:11111111@localhost:3306/online_courses_lab')

Session = sessionmaker(bind=engine)
session = Session()

student1 = Student(student_id=1, first_name="name", last_name="name1", email="asf@mail.com", password="12345", Gpa=3)
student2 = Student(student_id=2, first_name="name", last_name="name1", email="asf@mail.com", password="12345", Gpa=3)
professor1 = Professor(professor_id=1, first_name="name", last_name="name1", email="asf2@mail.com", password="12345", subject="math")
course1 = Course(course_id=1, professor_id=1, subject="math", professor=professor1)
course_student1 = Course_student(course_student_id=1, course_id=1, student_id=1, course=course1, student=student1)
course_student2 = Course_student(course_student_id=2, course_id=1, student_id=2, course=course1, student=student2)
join_request1 = Join_request(join_request_id=1, course_id=1, student_id=1, status="pending", course=course1, student=student1)

session.add_all([student1, professor1, course1, course_student1, join_request1, student2, course_student2])

session.commit()