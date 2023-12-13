from functools import wraps
from app.database import db


def db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {e}")
            raise

    return wrapper
