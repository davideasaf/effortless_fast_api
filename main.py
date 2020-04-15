"main.py"

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import config
from models.user import User as DBUser
from schemas.auth import Token
from schemas.user import User, UserWithPassword, UserCreate
from services.user import user_service
from utils.db_utils import get_db
from utils.security_utils.jwt import create_access_token
from utils.security_utils.route_dep import get_current_active_user, verify_admin_rights

api = FastAPI(title="Effortless Fast API")


@api.post("/login", response_model=Token, tags=["login"])
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_service.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            data={"id": user.user_id, "rls": user.roles},
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }


@api.get("/")
def hello_world():
    return "Hello World!"


@api.get(
    "/users-with-passwords",
    response_model=List[UserWithPassword],
    dependencies=[Depends(verify_admin_rights)],
    name="Get All Users (Admin Only)",
    tags=["Admin Only", "All Users Examples"],
    description="This is a summary for getting all users with passwords. But wouldn't it be nice if we could define a longer description? Use a docstring!",
    summary="Returns users WITH hashed password",
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return user_service.get_all(db)


# Hidden by using response_model to deserialize
@api.get(
    "/users-with-hidden-passwords-via-schema",
    response_model=List[User],
    tags=["All Users Examples"],
)
def get_all_users_hidden_pass_via_schema(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Gets all users without a password but uses the schema to mask the password 
    instead of doing it at the route

    # Also, this is valid markdown!
    """
    return user_service.get_all(db)


# Hidden by using response_model to deserialize
@api.get(
    "/users-with-hidden-passwords-via-exclude",
    response_model=List[UserWithPassword],
    response_model_exclude={"password"},
    description="Gets all users without a password. The password is hidden because the route specifically uses 'response_model_exclude'",
    tags=["All Users Examples"],
)
def get_all_users_hidden_pass_via_exclude(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return user_service.get_all(db)


@api.get(
    "/user/{user_id}", response_model=User,
)
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return user_service.get(db, id=user_id, id_name="user_id")


@api.get("hidden", include_in_schema=False)
def this_endpoint_is_hidden_from_docs():
    return "SHHHHHHH! This route exists but does not exist on OpenAPI docs🤫"


@api.post(
    "/user", response_model=User, tags=["Create Examples"],
)
def create_single_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    return user_service.create(db, obj_in=user_in)
