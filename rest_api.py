import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api, abort, marshal_with
from rest_models import app, db, Student, Professor, Course, Join_Request, Course_Student
from rest_models import rf_student, args_student, rf_professor, args_professor, rf_course, args_course, rf_join_request, args_join_request, rf_course_student, args_course_student
from rest_models import args_student_update, args_professor_update, args_course_update, args_join_request_update

api = Api(app)

class Students(Resource):
    @marshal_with(rf_student)
    def get(self, id):
        result = Student.query.get(id)
        if not result:
            abort(404, message="student does not exist")
        return result

    @marshal_with(rf_student)
    def post(self, id):
        arguments = args_student.parse_args()
        student = Student(first_name=arguments.first_name, last_name=arguments.last_name, email=arguments.email, password=arguments.password, GPA=arguments.GPA, iq=arguments.iq)
        db.session.add(student)
        db.session.commit()
        return student, 201    

    @marshal_with(rf_student)
    def patch(self, id):
        dict = {}
        args = args_student_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Student.query.filter_by(student_id=id)
        if not result.first():
            abort(404, message="student does not exist")
        result.update(dict)
        db.session.commit()
        return result.first(), 201     

    @marshal_with(rf_student)
    def delete(self, id):
        result = Student.query.filter_by(student_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="student does not exist")
        result.delete()
        db.session.commit()
        return deletedObj, 201
 

class Professors(Resource):
    @marshal_with(rf_professor)
    def get(self, id):
        result = Professor.query.get(id)
        if not result:
            abort(404, message="professor does not exist")
        return result

    @marshal_with(rf_professor)
    def post(self, id):
        arguments = args_professor.parse_args()
        professor = Professor(first_name=arguments.first_name, last_name=arguments.last_name, email=arguments.email, password=arguments.password, subject=arguments.subject)
        db.session.add(professor)
        db.session.commit()
        return professor, 201        

    @marshal_with(rf_professor)
    def patch(self, id):
        dict = {}
        args = args_professor_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Professor.query.filter_by(professor_id=id)
        if not result.first():
            abort(404, message="professor does not exist")
        result.update(dict)
        db.session.commit()
        return result.first(), 201 

    @marshal_with(rf_professor)
    def delete(self, id):
        result = Professor.query.filter_by(professor_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="professor does not exist")
        result.delete()
        db.session.commit()
        return deletedObj, 201

class Courses(Resource):
    @marshal_with(rf_course)
    def get(self, id):
        result = Course.query.get(id)
        if not result:
            abort(404, message="course does not exist")
        return result

    @marshal_with(rf_course)
    def post(self, id):
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
    def patch(self, id):
        dict = {}
        args = args_course_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        result = Course.query.filter_by(course_id=id)
        if not result.first():
            abort(404, message="course does not exist")

        if dict["professor_id"]:
           result = Professor.query.filter_by(professor_id=dict["professor_id"])
           courObj = result.first()
           if not courObj:
            abort(404, message="professor does not exist") 
            
        result.update(dict)
        db.session.commit()
        return result.first(), 201 

    @marshal_with(rf_course)
    def delete(self, id):
        result = Course.query.filter_by(course_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="course does not exist")
        result.delete()
        db.session.commit()
        return deletedObj, 201

class Join_Requests(Resource):
    @marshal_with(rf_join_request)
    def get(self, id):
        result = Join_Request.query.get(id)
        if not result:
            abort(404, message="join request does not exist")
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
    def patch(self, id):
        result = Join_Request.query.get(id)
        if result and (result.status == "success" or result.status == "error"):
            abort(400, message="join request already resolved")
        dict = {}
        args = args_join_request_update.parse_args()
        for arg in args:
            if (args[arg]):
               dict[arg] = args[arg]

        if dict["course_id"]:
           result = Course.query.filter_by(course_id=dict["course_id"])
           courObj = result.first()
           if not courObj:
            abort(404, message="course does not exist") 
 
        if dict["student_id"]:
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
    def delete(self, id):
        result = Join_Request.query.filter_by(join_request_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="join request does not exist")
        result.delete()
        db.session.commit()
        return deletedObj, 201

class Course_Students(Resource):
    @marshal_with(rf_course_student)
    def get(self, id):
        result = Course_Student.query.get(id)
        if not result:
            abort(404, message="course student does not exist")
        return result

    @marshal_with(rf_course_student)
    def post(self, id):
        arguments = args_course_student.parse_args()

        result = Course.query.filter_by(course_id=arguments.course_id)
        result1 = Student.query.filter_by(student_id=arguments.student_id)
        courObj = result.first()
        studObj = result1.first()
        if not studObj:
            abort(404, message="student does not exist")

        if not courObj:
            abort(404, message="course does not exist")   

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
    def delete(self, id):
        result = Course_Student.query.filter_by(course_student_id=id)
        deletedObj = result.first()
        if not deletedObj:
            abort(404, message="course student does not exist")
        result.delete()
        db.session.commit()
        return deletedObj, 201

class Courses_List(Resource):
    @marshal_with(rf_course)
    def get(self):
        result = Course.query.filter_by().all()
        return result

api.add_resource(Students, "/students/<int:id>")
api.add_resource(Professors, "/professors/<int:id>")
api.add_resource(Courses, "/courses/<int:id>")
api.add_resource(Courses_List, "/courses/")
api.add_resource(Join_Requests, "/join_requests/<int:id>")
api.add_resource(Course_Students, "/course_students/<int:id>")

if __name__ == "__main__":
    app.run(debug = True)