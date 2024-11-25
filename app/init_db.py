from sqlalchemy.exc import DBAPIError

from database import init_db


if __name__ == "__main__":
    try:
        init_db()
    except DBAPIError as e:
        print("Database already exists")
