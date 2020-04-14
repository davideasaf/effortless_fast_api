"DB utils"

from .session import Session


def get_db():
    """[summary]
    Generator function for dependency injection to fetch a 
    new sesesion on a new request
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()
