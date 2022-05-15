import requests
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from rest_models import app
from rest_api import api

token_professor = ""
professor_user = {}
course = {}


BASE = "http://127.0.0.1:5000/"
STUDENTS = "students/"
PROFESSORS = "professors/"
COURSES = "courses/"
JOIN_REQUESTS = "join_requests/"
COURSE_STUDENTS = "course_students/"
LOGIN = "login"

def setup_module(module):
    app.config['SECRET_KEY'] = 'lolsecret'

    global professor_user
    professor_user = requests.post(BASE+PROFESSORS+"0", {"first_name": "superComplicatedNameForLogi", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "superComplicatedPasswordForLogi", "subject": "meth"}).json();

    res2 = requests.post(BASE+LOGIN, auth=(professor_user['first_name'], professor_user['password']));

    global token_professor 
    token_professor = res2.json()["token"]

    global course
    course = requests.post(BASE+COURSES+"0", {"professor_id": professor_user["professor_id"], "subject": "meth"}, headers={'Authorization': token_professor}).json();
    pass    

def teardown_module(module):
    requests.delete(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': token_professor})
    requests.delete(BASE+COURSES+str(course['course_id']), headers={'Authorization': token_professor})
    pass

def test_get_course_list():
    res = requests.get(BASE+COURSES).json();
    assert course in res     
