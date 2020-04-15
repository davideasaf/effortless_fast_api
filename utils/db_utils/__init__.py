"DB utils"

from typing import Iterator
from .session import Session
from sqlalchemy.orm import Session as SqlAlchemySession


def get_db() -> Iterator[SqlAlchemySession]:
    """[summary]
    Generator function for dependency injection to fetch a 
    new sesesion on a new request
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()
