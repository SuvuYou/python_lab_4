import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api, abort, marshal_with
from flask import request, jsonify
from rest_models import app, db, Student, Professor, Course, Join_Request, Course_Student
from rest_models import  rf_student, args_student, rf_professor, args_professor, rf_course, args_course, rf_join_request, args_join_request, rf_course_student, args_course_student
from rest_models import args_student_update, args_professor_update, args_course_update, args_join_request_update
import jwt
import datetime
from functools import wraps

api = Api(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            abort(401, message="Token is missing")

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            if data['user_type'] == "student":
                current_user = Student.query.filter_by(student_id=data['public_id']).first()
            else:
                current_user = Professor.query.filter_by(professor_id=data['public_id']).first()    
        except:
            abort(401, message="Token is missing")

        current_user.user_type = data['user_type']

        return f(current_user, *args, **kwargs)

    return decorated

def basicStudentToObj (student):
    return {
    "student_id": student.student_id,
    "first_name": student.first_name,
    "last_name": student.last_name,
    "email": student.email,
    "password": student.password,
    "iq": student.iq,
    "GPA": student.GPA,
}  

class Students(Resource):    
    @marshal_with(rf_student)
    @token_required 
    def get(current_user, self, id):
        result = Student.query.get(id)
        if not result:
            abort(404, message="student does not exist")

        if not current_user.first_name == result.first_name:
            abort(403, message="Access denied")    
        return result

    @marshal_with(rf_student)
    def post(self, id):
        arguments = args_student.parse_args()
        result1 = Student.query.filter_by(email=arguments.email)
        result2 = Professor.query.filter_by(email=arguments.email)
        if result1.first() or result2.first() :
            abort(404, message="User with such email already exist")

        student = Student(first_name=arguments.first_name, last_name=arguments.last_name, email=arguments.email, password=arguments.password, GPA=arguments.GPA, iq=arguments.iq)
        db.session.add(student)
        db.session.commit()
        return student, 201    

    @marshal_with(rf_student)
    @token_required 
    def patch(current_user, self, id):
        dict = {}
        args = args_student_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Student.query.filter_by(student_id=id)
        if not result.first():
            abort(404, message="student does not exist")

        student = result.first()

        if not current_user.first_name == student.first_name:
            abort(403, message="Access denied")       
        
        result.update(dict)
        db.session.commit()
        return student, 201     

    @marshal_with(rf_student)
    @token_required 
    def delete(current_user, self, id):
        result = Student.query.filter_by(student_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="student does not exist")

        if not current_user.first_name == deletedObj.first_name:
            abort(403, message="Access denied")      
        result.delete()
        db.session.commit()
        return deletedObj, 201
 
def professorToObj (professor):
    return {
    "professor_id": professor.professor_id,
    "first_name": professor.first_name,
    "last_name": professor.last_name,
    "email": professor.email,
    "password": professor.password,
    "subject": professor.subject,
}  

class Professors(Resource):
    @marshal_with(rf_professor)
    @token_required 
    def get(current_user, self, id):
        result = Professor.query.get(id)
        if not result:
            abort(404, message="professor does not exist")

        if not current_user.first_name == result.first_name:
            abort(403, message="Access denied")          
        return result

    @marshal_with(rf_professor)
    def post(self, id):
        arguments = args_professor.parse_args()
        result1 = Student.query.filter_by(email=arguments.email)
        result2 = Professor.query.filter_by(email=arguments.email)
        if result1.first() or result2.first() :
            abort(404, message="User with such email already exist")

        professor = Professor(first_name=arguments.first_name, last_name=arguments.last_name, email=arguments.email, password=arguments.password, subject=arguments.subject)
        db.session.add(professor)
        db.session.commit()
        return professor, 201        

    @marshal_with(rf_professor)
    @token_required 
    def patch(current_user, self, id):
        dict = {}
        args = args_professor_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Professor.query.filter_by(professor_id=id)
        if not result.first():
            abort(404, message="professor does not exist")

        prof = result.first()

        if not current_user.first_name == prof.first_name:
            abort(403, message="Access denied")              
        result.update(dict)
        db.session.commit()
        return prof, 201 

    @marshal_with(rf_professor)
    @token_required
    def delete(current_user, self, id):
        result = Professor.query.filter_by(professor_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="professor does not exist")

        if not current_user.first_name == deletedObj.first_name:
            abort(403, message="Access denied")     
        result.delete()
        db.session.commit()
        return deletedObj, 201

class Courses(Resource):
    @token_required
    def get(current_user, self, id):
        course = basicCourseListToObj(Course.query.get(id))
        

        if not course:
            abort(404, message="course does not exist")

        if current_user.user_type == "professor" and course['professor_id'] != current_user.professor_id:
            abort(403, message="Access denied")  
        elif current_user.user_type == "student":
            course_student = Course_Student.query.filter_by(course_id=course['course_id'], student_id=current_user.student_id).first()
            if not course_student:
                abort(403, message="Access denied")  

        professor = Professor.query.get(course['professor_id'])
        course['professor'] = professorToObj(professor) 

        return course

    @marshal_with(rf_course)
    @token_required
    def post(current_user, self, id):
        if current_user.user_type == "student":
            abort(403, message="Access denied")  
        arguments = args_course.parse_args()
        result = Professor.query.filter_by(professor_id=arguments.professor_id)
        profObj = result.first()
        if not profObj:
            abort(404, message="professor does not exist")
        course = Course(professor_id=arguments.professor_id, subject=arguments.subject)
        db.session.add(course)
        db.session.commit()
        return course, 201

    @marshal_with(rf_course)
    @token_required
    def patch(current_user, self, id):
        dict = {}
        args = args_course_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Course.query.filter_by(course_id=id)
        if not result.first():
            abort(404, message="course does not exist")

        if current_user.user_type == "professor" and result.first().professor_id != current_user.professor_id:
            abort(403, message="Access denied")  
        elif current_user.user_type == "student":
            abort(403, message="Access denied")

        if "professor_id" in dict:
           result = Professor.query.filter_by(professor_id=dict["professor_id"])
           courObj = result.first()
           if not courObj:
            abort(404, message="professor does not exist") 
            
        result.update(dict)
        db.session.commit()
        return result.first(), 201 

    @marshal_with(rf_course)
    @token_required
    def delete(current_user, self, id):
        result = Course.query.filter_by(course_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="course does not exist")

        if current_user.user_type == "professor" and deletedObj.professor_id != current_user.professor_id:
            abort(403, message="Access denied")  
        elif current_user.user_type == "student":
            abort(403, message="Access denied")    
        result.delete()
        db.session.commit()
        return deletedObj, 201

def requestToObj (request):
    return {
    "join_request_id": request.join_request_id,
    "course_id": request.course_id,
    "student_id": request.student_id,
    "status": request.status
}  

class Join_Requests(Resource):
    @marshal_with(rf_join_request)
    @token_required
    def get(current_user, self, id):
        result = Join_Request.query.get(id)
        if not result:
            abort(404, message="join request does not exist")

        if current_user.user_type == "professor":
            course_professor = Course.query.filter_by(course_id=result.course_id, professor_id=current_user.professor_id).first()
            if not course_professor:
                abort(403, message="Access denied") 
        elif current_user.user_type == "student" and result.student_id != current_user.student_id:
            abort(403, message="Access denied")    
        return result

    @marshal_with(rf_join_request)
    def post(self, id):
        arguments = args_join_request.parse_args()

        result = Course.query.filter_by(course_id=arguments.course_id)
        result1 = Student.query.filter_by(student_id=arguments.student_id)
        courObj = result.first()
        studObj = result1.first()
        if not studObj:
            abort(404, message="student does not exist")

        if not courObj:
            abort(404, message="course does not exist")    

        join_request = Join_Request(course_id=arguments.course_id, student_id=arguments.student_id, status=arguments.status)

        same_join_request = Join_Request.query.filter_by(course_id=arguments['course_id'], student_id=arguments['student_id'])

        if same_join_request.first():
            abort(400, message="can't add join request, join request is already created")

        students_in_course = Course_Student.query.filter_by(course_id=arguments['course_id'])
        if len(students_in_course.all()) >= 5:
            abort(400, message="can't add student, course is full")
       
        for student in students_in_course.all():
            if student.student_id == arguments['student_id']:
                abort(400, message="student is already added")

        db.session.add(join_request)
        db.session.commit()
        return join_request, 201   

    @marshal_with(rf_join_request)
    @token_required
    def patch(current_user, self, id):
        result = Join_Request.query.get(id)

        if current_user.user_type == "professor":
            course_professor = Course.query.filter_by(course_id=result.course_id, professor_id=current_user.professor_id).first()
            if not course_professor:
                abort(403, message="Access denied") 
        elif current_user.user_type == "student":
            abort(403, message="Access denied")    

        if result and (result.status == "success" or result.status == "error"):
            abort(400, message="join request already resolved")
        dict = {}
        args = args_join_request_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        if hasattr(dict, "course_id"):
           result = Course.query.filter_by(course_id=dict["course_id"])
           courObj = result.first()
           if not courObj:
            abort(404, message="course does not exist") 
 
        if hasattr(dict, "student_id"):
           result = Student.query.filter_by(student_id=dict["student_id"])
           studObj = result.first()
           if not studObj:
            abort(404, message="student does not exist")         

        result = Join_Request.query.filter_by(join_request_id=id)
        if not result.first():
            abort(404, message="join request does not exist")
        result.update(dict)

        new_request = result.first()
        if new_request.status == "success":
            course_student = Course_Student(course_id=new_request.course_id, student_id=new_request.student_id)
            db.session.add(course_student)

        db.session.commit()
        return result.first(), 201 

    @marshal_with(rf_join_request)
    @token_required
    def delete(current_user, self, id):
        result = Join_Request.query.filter_by(join_request_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="join request does not exist")

        if current_user.user_type == "professor":
            course_professor = Course.query.filter_by(course_id=result.course_id, professor_id=current_user.professor_id).first()
            if not course_professor:
                abort(403, message="Access denied") 
        elif current_user.user_type == "student":
            abort(403, message="Access denied")    
        result.delete()
        db.session.commit()
        return deletedObj, 201

def requestsListToObj (course):
    return {
    "course_id": course.course_id,
    "professor_id": course.professor_id,
    "subject": course.subject,
}  

class Requests_List(Resource):
    @token_required 
    def get(current_user, self):
        if current_user.user_type == 'student':
            student = basicStudentToObj(Student.query.get(current_user.student_id))
            joinRequests = Join_Request.query.filter_by(student_id=current_user.student_id).all()
            objJoinRequests = list(map(lambda x: requestToObj(x), joinRequests)) 

            allRequests = []
            for request in objJoinRequests:
                course = basicCourseListToObj(Course.query.filter_by(course_id=request['course_id']).first())
                professor = professorToObj(Professor.query.get(course['professor_id']))
                course['professor'] = professor
                request['course'] = course
                request['student'] = student
                allRequests.append(request)

            parsedRequests = list(map(lambda x: x, allRequests))
        else:
            professor = professorToObj(Professor.query.get(current_user.professor_id))
            professorCourses = Course.query.filter_by(professor_id=current_user.professor_id)
            professorCoursesIds = list(map(lambda x: x.course_id, professorCourses)) 
            joinRequests = Join_Request.query.filter(Course.course_id.in_(professorCoursesIds))
            objJoinRequests = list(map(lambda x: requestToObj(x), joinRequests)) 

            allRequests = []
            for request in objJoinRequests:
                student = basicStudentToObj(Student.query.get(request['student_id']))
                course = basicCourseListToObj(Course.query.filter_by(course_id=request['course_id']).first())
                course['professor'] = professor
                request['course'] = course
                request['student'] = student
                if request['status'] == 'pending':
                    allRequests.append(request)

            parsedRequests = list(map(lambda x: x, allRequests)) 

        return jsonify({'requests' : parsedRequests})        

class Course_Students(Resource):
    @marshal_with(rf_course_student)
    def get(self, id):
        result = Course_Student.query.get(id)
        if not result:
            abort(404, message="course student does not exist")
        return result

    @marshal_with(rf_course_student)
    @token_required
    def post(current_user, self, id):
        arguments = args_course_student.parse_args()

        result = Course.query.filter_by(course_id=arguments.course_id)
        result1 = Student.query.filter_by(student_id=arguments.student_id)
        courObj = result.first()
        studObj = result1.first()
        if not studObj:
            abort(404, message="student does not exist")

        if not courObj:
            abort(404, message="course does not exist")   

        if current_user.user_type == "professor":
            course_professor = Course.query.filter_by(course_id=courObj.course_id, professor_id=current_user.professor_id).first()
            if not course_professor:
                abort(403, message="Access denied") 
        elif current_user.user_type == "student":
            abort(403, message="Access denied")      

        course_student = Course_Student(course_id=arguments['course_id'], student_id=arguments['student_id'])
        students_in_course = Course_Student.query.filter_by(course_id=arguments['course_id'])
        if len(students_in_course.all()) >= 5:
            abort(400, message="can't add student, course is full")
       
        for student in students_in_course.all():
            if student.student_id == arguments['student_id']:
                abort(400, message="student is already added")
      
        db.session.add(course_student)
        db.session.commit()
        return course_student, 201 

    @marshal_with(rf_course_student)
    @token_required
    def delete(current_user, self, id):
        result = Course_Student.query.filter_by(course_student_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="course student does not exist")

        if current_user.user_type == "professor":
            course_professor = Course.query.filter_by(course_id=deletedObj.course_id, professor_id=current_user.professor_id).first()
            if not course_professor:
                abort(403, message="Access denied") 
        elif current_user.user_type == "student":
            abort(403, message="Access denied")          
        result.delete()
        db.session.commit()
        return deletedObj, 201

def basicCourseListToObj (course):
    return {
    "course_id": course.course_id,
    "professor_id": course.professor_id,
    "subject": course.subject,
}  

def courseListToObj (course):
    return {
    "course_id": course['course_id'],
    "professor_id": course['professor_id'],
    "professor": course['professor'],
    "subject": course['subject'],
}  

class Courses_List(Resource):
    @token_required 
    def get(current_user, self):
        if current_user.user_type == 'student':
            studentsCourses = Course_Student.query.filter_by(student_id=current_user.student_id)
            allBasicCourses = list(map(lambda x: basicCourseListToObj(x), Course.query.filter_by().all())) 
            allCourses = []
            for course in allBasicCourses:
                professor = Professor.query.get(course['professor_id'])
                course['professor'] = professorToObj(professor)
                allCourses.append(course)


            allCourses = list(map(lambda x: courseListToObj(x), allCourses)) 
            allIds = list(map(lambda x: x.course_id, studentsCourses))

            freeCourses = list(filter(lambda x: (x['course_id'] not in allIds), allCourses))
            freeCoursesWithRequests = []

            for course in freeCourses:
                request = Join_Request.query.filter_by(student_id=current_user.student_id, course_id=course['course_id']).first()
                if request:
                    req = requestToObj(request)
                    course['request'] = req
                freeCoursesWithRequests.append(course) 

            parsedJoinedCourses = list(filter(lambda x: (x['course_id'] in allIds), allCourses));
            parsedFreeCourses = freeCoursesWithRequests    
            
        else:
            professor = Professor.query.get(current_user.professor_id)
            professorCourses = Course.query.filter_by(professor_id=current_user.professor_id)
            allJoinedCourses = list(map(lambda x: basicCourseListToObj(x), professorCourses)) 
            allCourses = []
            for course in allJoinedCourses:
                course['professor'] = professorToObj(professor)
                allCourses.append(course)

            parsedJoinedCourses = list(map(lambda x: courseListToObj(x), allCourses)) 
            parsedFreeCourses = []

        return jsonify({'joined' : parsedJoinedCourses , "free": parsedFreeCourses})


class Login(Resource):
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            abort(401, message="Could not verify")

        user = Student.query.filter_by(email=auth.username).first()

        if user: 
            user_type = "student"
        else:
            user = Professor.query.filter_by(email=auth.username).first()
            user_type = "professor"

        if not user:
            abort(401, message="User doesn't exist")

        if user_type == "student":
            pub_id = user.student_id
        else:
            pub_id = user.professor_id     

        userData = {}
        if user_type == "student":
            userData = {'id': user.student_id, "firstName": user.first_name, "lastName": user.last_name, "type": user_type}
        else:
            userData = {'id': user.professor_id, "firstName": user.first_name, "lastName": user.last_name, "type": user_type} 

        if user.password == auth.password:
            token = jwt.encode({'public_id' : pub_id, "user_type": user_type, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
  
            return jsonify({'token' : token, "user": userData})
           

        abort(401, message="Could not verify")
      

api.add_resource(Students, "/students/<int:id>")
api.add_resource(Professors, "/professors/<int:id>")
api.add_resource(Courses, "/courses/<int:id>")
api.add_resource(Courses_List, "/courses_list")
api.add_resource(Requests_List, "/requests_list")
api.add_resource(Join_Requests, "/join_requests/<int:id>")
api.add_resource(Course_Students, "/course_students/<int:id>")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug = True)