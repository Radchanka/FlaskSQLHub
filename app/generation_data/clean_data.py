from app.main import create_app
from app.database import db
from app.models import Group, Student, Course, student_course_association
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(wait=wait_fixed(1000), stop=stop_after_attempt(3))
def delete_data():
    app = create_app()

    with app.app_context():
        try:

            db.session.execute(student_course_association.delete())

            db.session.query(Student).delete()

            db.session.query(Group).delete()

            db.session.query(Course).delete()

            db.session.commit()

            print("Database cleared")
        except Exception as e:
            db.session.rollback()
            print(f"Error while clearing database: {e}")
            raise


if __name__ == '__main__':
    delete_data()
