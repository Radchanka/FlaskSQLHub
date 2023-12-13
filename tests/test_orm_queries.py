import unittest
from app.main import create_app
from app.queries import *


class TestORMQueries(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app_context = create_app().app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_find_groups_with_students_limit(self):
        group1 = Group(name='Group1')
        group2 = Group(name='Group2')

        student1 = Student(first_name='John', last_name='Doe', group=group1)
        student2 = Student(first_name='Jane', last_name='Smith', group=group1)
        student3 = Student(first_name='Bob', last_name='Johnson', group=group2)

        db.session.add_all([group1, group2, student1, student2, student3])
        db.session.commit()

        result = find_groups_with_students_limit(2)

        unique_group_ids = {group.id for group in result}
        self.assertEqual(len(unique_group_ids), 2)

    def test_find_students_by_course_name(self):
        course1 = Course(name='Math')
        course2 = Course(name='Biology')

        student1 = Student(first_name='John', last_name='Doe')
        student2 = Student(first_name='Jane', last_name='Smith')

        student1.courses.append(course1)
        student2.courses.append(course2)

        db.session.add_all([course1, course2, student1, student2])
        db.session.commit()

        result = find_students_by_course_name('Math')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].first_name, 'John')

    def test_add_new_student(self):
        group = Group(name='TestGroup')
        db.session.add(group)
        db.session.commit()

        add_new_student('New', 'Student', group.id)

        result = db.session.query(Student).filter_by(first_name='New', last_name='Student').first()
        self.assertIsNotNone(result)

    def test_remove_student_from_course(self):
        group = Group(name='Group1')
        course = Course(name='Math', description='Math course')
        student = Student(first_name='John', last_name='Doe', group=group)

        student.courses.append(course)

        db.session.add_all([group, course, student])
        db.session.commit()

        result = remove_student_from_course(student.id, course.name)

        self.assertTrue(result)
        self.assertEqual(len(student.courses), 0)

    def test_add_student_to_course(self):
        student = Student(first_name='John', last_name='Doe')
        course = Course(name='Math', description='Mathematics course')
        db.session.add_all([student, course])
        db.session.commit()

        add_student_to_course(student.id, course.name)

        result = db.session.query(Student).filter_by(id=student.id).first()
        self.assertIn(course, result.courses)


if __name__ == '__main__':
    unittest.main()
