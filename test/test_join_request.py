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
join_request = {}

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
    
    global join_request
    join_request = requests.post(BASE+JOIN_REQUESTS+"0", {"course_id": course['course_id'], "student_id": student_user['student_id'], "status": "pending"}).json();
    
    pass    

def teardown_module(module):
    requests.delete(BASE+JOIN_REQUESTS+str(join_request['join_request_id']), headers={'Authorization': token_professor})
    requests.delete(BASE+COURSES+str(course['course_id']), headers={'Authorization': token_professor})
    requests.delete(BASE+STUDENTS+str(student_user['student_id']), headers={'Authorization': token_student})
    requests.delete(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': token_professor})
    pass

def test_post_join_request_student_doesnt_exist():
    res = requests.post(BASE+JOIN_REQUESTS+"0", {"course_id": course['course_id'], "student_id": "1000000000", "status": "pending"}).json();
    assert res == {"message": "student does not exist"}

def test_post_join_request_course_doesnt_exist():
    res = requests.post(BASE+JOIN_REQUESTS+"0", {"course_id": "1000000000", "student_id": student_user['student_id'], "status": "pending"}).json();
    assert res == {"message": "course does not exist"}

def test_post_join_request_already_created():
    res = requests.post(BASE+JOIN_REQUESTS+"0", {"course_id": course['course_id'], "student_id": student_user['student_id'], "status": "pending"}).json();
    assert res == {"message": "can't add join request, join request is already created"}

def test_patch_join_request_resolve():
    res = requests.patch(BASE+JOIN_REQUESTS+str(join_request['join_request_id']), {"status": "success"}, headers={'Authorization': token_professor}).json();
    assert res['status'] == "success"  

def test_patch_join_request_already_resolved():
    res = requests.patch(BASE+JOIN_REQUESTS+str(join_request['join_request_id']), {"status": "error"}, headers={'Authorization': token_professor}).json();
    assert res == {"message": "join request already resolved"}     
       
def test_get_join_request_doesnt_exist():
    res = requests.get(BASE+JOIN_REQUESTS+"100000000", headers={'Authorization': token_professor}).json();
    assert res == {"message": "join request does not exist"}     

def test_get_join_request_access_denied():
    res = requests.patch(BASE+JOIN_REQUESTS+str(join_request['join_request_id']), {"status": "error"}, headers={'Authorization': token_student}).json();
    assert res == {"message": "Access denied"}       