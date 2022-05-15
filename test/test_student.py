import requests
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from rest_api import app
from flask import current_app

token = ""
global student_user

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
    pass    

def teardown_module(module):
    requests.delete(BASE+STUDENTS+str(student_user['student_id']), headers={'Authorization': token})
    pass

def test_login_could_not_verify():
    res = requests.post(BASE+LOGIN, auth=("randomName", "randomPassword")).json();
    assert res == {"message": "Could not verify"} 

def test_login_as_student():
    res = requests.post(BASE+LOGIN, auth=(student_user['first_name'], student_user['password']));
    global token 
    token = res.json()["token"]
    assert res.status_code == 200
    assert type(token) is str

def test_get_student():
    res = requests.get(BASE+STUDENTS+str(student_user['student_id']), headers={'Authorization': token}).json();
    assert student_user == res

def test_get_student_doesnt_exist():
    res = requests.get(BASE+STUDENTS+"10000000", headers={'Authorization': token}).json();
    assert res == {"message": "student does not exist"}

def test_get_student_token_is_missing():
    res = requests.get(BASE+STUDENTS+str(student_user['student_id']), headers={'Authorization': "randomtokent"}).json();
    assert res == {"message": "Token is missing"}  
       
def test_patch_student():
    field = "newLastName"
    res = requests.patch(BASE+STUDENTS+str(student_user['student_id']), {"last_name": field}, headers={'Authorization': token}).json();
    assert field == res["last_name"]  