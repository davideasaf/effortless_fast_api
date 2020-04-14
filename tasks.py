"tasks to be invoked via Invoke python"
import os
from invoke import task

HEROKU_APP_NAME = "YOUR-HEROKU-APP-HERE"


def get_db_url(ctx) -> str:
    """Get db url with local heroku setup

    Args:
        ctx (Context): Invoke context

    Returns:
        str: connection string for db
    """
    return ctx.run(
        f"heroku config:get DATABASE_URL -a {HEROKU_APP_NAME}"
    ).stdout.strip()


@task
def start(ctx, host="127.0.0.1", port=5000, reload=True):
    """Start the backend as a dev server or production ready gunicorn server"""

    reload_flag = "--reload" if reload else ""

    ctx.run(
        f"""
        uvicorn main:api {reload_flag} --port {port} --host {host}
        """,
        pty=True,
        echo=True,
    )


@task
def init_db(ctx, config_name="dev"):
    """Initialize Database"""
    from utils.db_utils.session import db_session, engine
    from utils.db_utils.base_class import Base
    from sqlalchemy.orm import Session
    from models import User

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@task
def seed_db(ctx, config_name="dev"):
    """Initialize Database"""
    from models.user import User
    from utils.security_utils import get_password_hash
    from utils.db_utils.session import db_session
    from schemas.user import UserCreate
    from services.user import user_service

    user_service.create(
        db_session,
        obj_in=UserCreate(username="admin", password="password", roles="admin"),
    )

    user_service.create(db_session, obj_in=UserCreate(username="user", password="pass"))
