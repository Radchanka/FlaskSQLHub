from app.database import db

student_course_association = db.Table(
    'student_course_association',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    students = db.relationship('Student', backref='group', lazy=True)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    courses = db.relationship(
        'Course',
        secondary='student_course_association',
        back_populates='students'
    )


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    students = db.relationship(
        'Student',
        secondary='student_course_association',
        back_populates='courses'
    )
