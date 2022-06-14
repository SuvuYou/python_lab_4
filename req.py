import requests

BASE = "http://127.0.0.1:5000/"
STUDENTS = "students/"
PROFESSORS = "professors/"
COURSES = "courses/"
JOIN_REQUESTS = "join_requests/"
COURSE_STUDENTS = "course_students/"


# succ
# responce = requests.post(BASE + COURSES, {})
# succ
# responce = requests.post(BASE + STUDENTS + "0", {"first_name": "some name1", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "qweqweqwe", "iq": 100, "GPA": 5})
# succ

# responce = requests.post(BASE + "login", auth=("name", "123456"))

# responce = requests.post(BASE + PROFESSORS + "0", {"first_name": "some name1", "last_name": "some last name1", "email": "someemail@gmail.com", "password": "qweqweqwe", "subject": "Litrature"})
# succ
# responce = requests.delete(BASE + COURSES + "20")

# student already added
# responce = requests.post(BASE + JOIN_REQUESTS + "0", {"course_id": 30, "student_id": 8, "status":"pending"})
# full course
# responce = requests.post(BASE + JOIN_REQUESTS + "0", {"course_id": 1, "student_id": 3, "status":"pending"})
# succ
# responce = requests.patch(BASE + JOIN_REQUESTS + "4", {"status":"success"})

# responce = requests.post(BASE + COURSES + "0", {"professor_id": 100, "subject": "math"})
# responce = requests.post(BASE + JOIN_REQUESTS + "0", {"course_id": 1, "student_id": 32, "status":"pending"})
# responce = requests.post(BASE + COURSE_STUDENTS + "0", {"course_id": 122, "student_id": 3})
# responce = requests.patch(BASE + JOIN_REQUESTS + "6", {"course_id": 1, "student_id": 32})
# responce = requests.post(BASE + "login", {"username": "asdeged"})

print(responce)    
if 'json' in responce.headers.get('Content-Type'):
    js = responce.json()
else:
    print('Response content is not in JSON format.')
    print(responce)
    js = 'spam'
print(js)    