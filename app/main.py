from flask import Flask
from flask_restful import Api
from sqlalchemy import inspect
from app.database import db
from app.resources import GroupResource, StudentResource, CourseResource


def create_app():
    app = Flask(__name__)

    # Configure database connection
    db_config = {
        'user': 'myappuser',
        'password': 'qwerty',
        'host': 'localhost',
        'database': 'mydatabase'
    }

    app.config['SQLALCHEMY_DATABASE_URI'] = generate_connection_string(db_config)
    db.init_app(app)

    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        for table_name in ['group', 'student', 'course', 'student_course_association']:
            if table_name not in existing_tables:
                db.metadata.tables[table_name].create(bind=db.engine)

    api = Api(app)
    api.add_resource(GroupResource, '/group/<int:group_id>')
    api.add_resource(StudentResource, '/student/<int:student_id>', '/student/')
    api.add_resource(CourseResource, '/course/<string:course_name>')

    return app


def generate_connection_string(config):
    """
    Generate SQLAlchemy connection string based on the given configuration.
    """
    return f"postgresql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
