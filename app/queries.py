from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.config import GROUPS_WITH_STUDENTS_LIMIT
from app.db_decorators import db_session
from app.models import db, Student, Group, Course


@db_session
def find_groups_with_students_limit(limit: GROUPS_WITH_STUDENTS_LIMIT) -> list[Group]:
    try:
        result = db.session.query(Group). \
            join(Group.students). \
            group_by(Group). \
            having(func.count(Student.id) <= limit). \
            all()
        return result
    except Exception as e:
        print(f"Error in find_groups_with_students_limit: {e}")
        return []


@db_session
def find_students_by_course_name(course_name: str) -> list[Student]:
    try:
        students = Student.query.join(Student.courses).filter(Course.name == course_name).all()
        return students
    except Exception as e:
        print(f"Error in find_students_by_course_name: {e}")
        return []


@db_session
def add_new_student(first_name: str, last_name: str, group_id: int):
    try:
        group = db.session.get(Group, group_id)
        if group:
            new_student = Student(first_name=first_name, last_name=last_name, group=group)
            db.session.add(new_student)
            return new_student
        else:
            raise ValueError(f"Group with ID {group_id} not found.")
    except Exception as e:
        print(f"Error in add_new_student: {e}")
        raise


@db_session
def delete_student_by_id(student_id: int) -> bool:
    try:
        student = db.session.get(Student, student_id)
        if student:
            db.session.delete(student)
            return True
        else:
            raise ValueError(f"Student with ID {student_id} not found.")
    except Exception as e:
        print(f"Error in delete_student_by_id: {e}")
        raise


@db_session
def add_student_to_course(student_id: int, course_name: str) -> bool:
    try:
        student = Student.query.get(student_id)
        course = Course.query.filter_by(name=course_name).first()

        if not student or not course:
            raise ValueError("Invalid student or course")

        student.courses.append(course)
        return True
    except SQLAlchemyError as e:
        print(f"Database error in add_student_to_course: {e}")
        raise
    except Exception as e:
        print(f"Error in add_student_to_course: {e}")
        raise


@db_session
def remove_student_from_course(student_id: int, course_name: str) -> bool:
    try:
        student = db.session.get(Student, student_id)
        course = Course.query.filter_by(name=course_name).first()

        if student and course:
            student.courses.remove(course)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in remove_student_from_course: {e}")
        raise
