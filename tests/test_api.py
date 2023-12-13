import unittest
from flask_testing import TestCase

from app.main import create_app
from app.models import *


class TestAPI(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myappuser:qwerty@localhost/test_database'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_existing_student(self):
        group = Group(name='TestGroup')
        db.session.add(group)

        existing_student = Student(first_name='John', last_name='Doe', group=group)
        db.session.add(existing_student)
        db.session.commit()

        response = self.client.get(f'/student/{existing_student.id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['student_id'], existing_student.id)
        self.assertEqual(data['first_name'], existing_student.first_name)
        self.assertEqual(data['last_name'], existing_student.last_name)

    def test_get_nonexistent_student(self):
        response = self.client.get('/student/999')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Student not found')

    def test_get_existing_course(self):
        course = Course(name='TestCourse', description='Test description')
        db.session.add(course)
        db.session.commit()

        response = self.client.get(f'/course/{course.name}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['course_name'], course.name)
        self.assertEqual(data['course_description'], course.description)

    def test_get_nonexistent_course(self):
        response = self.client.get('/course/NonexistentCourse')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Course not found')


if __name__ == '__main__':
    unittest.main()
