from typing import Optional

from sqlalchemy.orm import Session

from models import User
from schemas.user import UserCreate, UserUpdate
from utils.security_utils import verify_password, get_password_hash
from .base import CRUDBase


class UserService(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db_session: Session, *, username: str) -> Optional[User]:
        return db_session.query(User).filter(User.username == username).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            **obj_in.dict(exclude={"password"}),
            password=get_password_hash(obj_in.password),
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db_session: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db_session, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_service = UserService(User)
