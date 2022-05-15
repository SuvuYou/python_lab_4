import requests
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from rest_models import app
from rest_api import api

token_student = ""
token_professor = ""
student_user = {}
professor_user = {}
course = {}
course_student = {}

BASE = "http://127.0.0.1:5000/"
STUDENTS = "students/"
PROFESSORS = "professors/"
COURSES = "courses/"
JOIN_REQUESTS = "join_requests/"
COURSE_STUDENTS = "course_students/"
LOGIN = "login"

def setup_module(module):
    app.config['SECRET_KEY'] = 'lolsecret'
    global student_user
    student_user = requests.post(BASE+STUDENTS+"0", {"first_name": "superComplicatedNameForLogin", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "superComplicatedPasswordForLogin", "iq": 100, "GPA": 5}).json();
    
    global professor_user
    professor_user = requests.post(BASE+PROFESSORS+"0", {"first_name": "superComplicatedNameForLogi", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "superComplicatedPasswordForLogi", "subject": "meth"}).json();
     
    res = requests.post(BASE+LOGIN, auth=(student_user['first_name'], student_user['password']));
    global token_student 
    token_student = res.json()["token"]

    res2 = requests.post(BASE+LOGIN, auth=(professor_user['first_name'], professor_user['password']));

    global token_professor 
    token_professor = res2.json()["token"]

    global course
    course = requests.post(BASE+COURSES+"0", {"professor_id": professor_user["professor_id"], "subject": "meth"}, headers={'Authorization': token_professor}).json();
    
    global course_student
    course_student = requests.post(BASE+COURSE_STUDENTS+"0", {"course_id": course["course_id"], "student_id": student_user["student_id"]}, headers={'Authorization': token_professor}).json();
    pass    

def teardown_module(module):
    requests.delete(BASE+COURSES+str(course['course_id']), headers={'Authorization': token_professor})
    requests.delete(BASE+STUDENTS+str(student_user['student_id']), headers={'Authorization': token_student})
    requests.delete(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': token_professor})
    pass

def test_get_course_student_doesnt_exist():
    res = requests.get(BASE+COURSE_STUDENTS+"100000000").json();
    assert res == {"message": "course student does not exist"}     

def test_post_course_student_access_denied():
    res = requests.post(BASE+COURSE_STUDENTS+"0", {"course_id": course['course_id'], "student_id": "1000000000"}, headers={'Authorization': token_student}).json();
    assert res == {"message": "student does not exist"}

def test_post_course_student_student_doesnt_exist():
    res = requests.post(BASE+COURSE_STUDENTS+"0", {"course_id": "1000000000", "student_id": student_user['student_id']}, headers={'Authorization': token_student}).json();
    assert res == {"message": "course does not exist"}

def test_post_course_student_student_access_denied():
    res = requests.post(BASE+COURSE_STUDENTS+"0", {"course_id": course['course_id'], "student_id": student_user['student_id']}, headers={'Authorization': token_student}).json();
    assert res == {"message": "Access denied"}    

def test_post_course_student_already_added():
    res = requests.post(BASE+COURSE_STUDENTS+"0", {"course_id": course['course_id'], "student_id": student_user['student_id'], "status": "pending"}, headers={'Authorization': token_professor}).json();
    assert res == {"message": "student is already added"}

def test_delete_course_student_doesnt_exist():
    res = requests.delete(BASE+COURSE_STUDENTS+"100000000", headers={'Authorization': token_professor}).json();
    assert res == {"message": "course student does not exist"}       