"Security Utils"

from enum import Enum
from typing import List

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

import config
from models.user import User
from schemas.auth import TokenPayload
from services.user import user_service
from utils.db_utils import get_db
from utils.security_utils.jwt import ALGORITHM


class UserRoles(str, Enum):
    """[summary]
    User Roles
    """

    admin = "admin"


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Security(OAuth2PasswordBearer(tokenUrl="/login")),
):
    """[summary]
    Fetches current user from token. gets user id from token and fetches from DB
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = user_service.get(db, id=token_data.id, id_name="user_id")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    """[summary]
    from get_current_user, validates the user is active
    """
    if not user_service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RolesAccepted:
    """[summary]
    Class that can be used within FastAPI dependency injection.
    Example: Depends(RolesAccepted(["role_1", "role_2"]))
    
    """

    def __init__(self, roles: List[str]):
        self.roles = roles

    def __call__(self, current_user: User = Security(get_current_user)):
        for admitted_role in self.roles:
            if admitted_role == current_user.roles:
                return True

        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privilege"
        )


async def verify_admin_rights(
    is_admin: bool = Depends(RolesAccepted([UserRoles.admin])),
):
    """[summary]
    Validates that the user contains admin rights
    """
    return is_admin
