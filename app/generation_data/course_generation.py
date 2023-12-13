import json
from app.config import COURSES_DATA_FILE_PATH
from app.models import Course


def generate_courses(file_path: str) -> list[Course]:
    with open(file_path, 'r') as file:
        course_data = json.load(file)

    courses = [Course(name=data['name'], description=data['description']) for data in course_data]
    return courses


if __name__ == '__main__':
    courses = generate_courses(COURSES_DATA_FILE_PATH)
