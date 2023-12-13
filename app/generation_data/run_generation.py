from course_generation import generate_courses
from group_generation import generate_groups
from student_generation import generate_students
from app.main import create_app
from app.database import db
from app.config import COURSES_DATA_FILE_PATH


def run_generation():
    try:
        app = create_app()

        with app.app_context():

            courses = generate_courses(COURSES_DATA_FILE_PATH)
            groups = generate_groups()
            students = generate_students(groups, courses)

            db.session.add_all(groups)
            db.session.add_all(courses)
            db.session.add_all(students)
            db.session.commit()

        print("Data has been successfully added to the database.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    run_generation()
