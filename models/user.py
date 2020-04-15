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

    def __repr__(self):
        return f"<User {self.user_id} - {self.username}>"
