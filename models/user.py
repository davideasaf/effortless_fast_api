"User Model"
# pylint: disable=no-member
from utils.db_utils.base_class import Base
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, Text, Column, Boolean, DateTime

# A generic user model that might be used by an app powered by flask-praetorian
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    roles = Column(Text)
    is_active = Column(Boolean, default=True, server_default="true")
    created_datetime = Column(DateTime(), nullable=False, server_default=func.now())

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, user_id: int):
        return cls.query.get(user_id)

    @property
    def identity(self):
        return self.user_id

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return f"<User {self.user_id} - {self.username}>"
