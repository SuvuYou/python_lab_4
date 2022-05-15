import requests
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from rest_models import app


token = ""
global professor_user

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
    professor_user = requests.post(BASE+PROFESSORS+"0", {"first_name": "superComplicatedNameForLogi2", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "superComplicatedPasswordForLogi2", "subject": "meth"}).json();
    pass    

def teardown_module(module):
    requests.delete(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': token})
    pass

def test_login_as_professor():
    res = requests.post(BASE+LOGIN, auth=(professor_user['first_name'], professor_user['password']));
    global token 
    token = res.json()["token"]
    assert res.status_code == 200
    assert type(token) is str

def test_get_professor():
    res = requests.get(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': token}).json();
    assert "subject" in res.keys()

def test_get_professor_doesnt_exist():
    res = requests.get(BASE+PROFESSORS+"10000000", headers={'Authorization': token}).json();
    assert res == {"message": "professor does not exist"}

def test_get_professor_token_is_missing():
    res = requests.get(BASE+PROFESSORS+str(professor_user['professor_id']), headers={'Authorization': "randomtokent"}).json();
    assert res == {"message": "Token is missing"}  
       
def test_patch_professor():
    field = "newLastName"
    res = requests.patch(BASE+PROFESSORS+str(professor_user['professor_id']), {"last_name": field}, headers={'Authorization': token}).json();
    assert field == res["last_name"]  