"SQLAlchemy Base Class"

from sqlalchemy.ext.declarative import declarative_base


class CustomBase(object):
    """[summary]
    Base class for SQLAlchemy model
    """

    # Generate __tablename__ automatically
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
