from flask_restful import Resource, reqparse

from app.db_decorators import db_session
from app.models import Group, Student, Course
from app.database import db


class GroupResource(Resource):
    @db_session
    def get(self, group_id):
        group = Group.query.get(group_id)
        if group:
            return {'group_id': group.id, 'group_name': group.name}, 200
        else:
            return {'message': 'Group not found'}, 404


class StudentResource(Resource):
    @db_session
    def get(self, student_id):
        student = Student.query.get(student_id)
        if student:
            return {'student_id': student.id, 'first_name': student.first_name, 'last_name': student.last_name}, 200
        else:
            return {'message': 'Student not found'}, 404

    @db_session
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('group_id', type=int, required=True)
        args = parser.parse_args()

        group = Group.query.get(args['group_id'])
        if group:
            new_student = Student(first_name=args['first_name'], last_name=args['last_name'], group=group)
            db.session.add(new_student)
            db.session.commit()
            return {'message': 'Student added successfully'}, 201
        else:
            return {'message': 'Group not found'}, 404


class CourseResource(Resource):
    @db_session
    def get(self, course_name):
        course = Course.query.filter_by(name=course_name).first()
        if course:
            return {'course_name': course.name, 'course_description': course.description}, 200
        else:
            return {'message': 'Course not found'}, 404
