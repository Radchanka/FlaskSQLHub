import random
from app.models import Student, Group, Course
from course_generation import generate_courses
from group_generation import generate_groups


def generate_students(groups: list[Group], courses: list[Course]) -> list[Student]:
    first_names = ['John', 'Alice', 'Bob', 'Eve', 'Charlie', 'Grace', 'David', 'Olivia', 'Sophia', 'Henry']
    last_names = ['Smith', 'Johnson', 'Lee', 'Brown', 'Davis', 'Wang', 'Kim', 'Garcia', 'Martinez', 'Lopez']
    students = []

    for group in groups:

        num_students_in_group = random.randint(10, 30)

        for _ in range(num_students_in_group):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            student = Student(first_name=first_name, last_name=last_name)
            students.append(student)
            group.students.append(student)

            num_courses = random.randint(1, 3)
            student.courses = random.sample(courses, num_courses)

    return students


if __name__ == '__main__':
    courses = generate_courses()
    groups = generate_groups()
    students = generate_students(groups, courses)
