"JWT"
from datetime import datetime, timedelta
from uuid import uuid4

import jwt

import config

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """[summary]
    Creates a JWT access token. This currently matches base flask-praetorian defaults
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    refresh_exp = datetime.utcnow() + timedelta(weeks=4)
    to_encode.update(
        {
            "iat": datetime.utcnow(),
            "exp": expire,
            "sub": access_token_jwt_subject,
            "jti": str(uuid4()),
            "rf_exp": int(refresh_exp.timestamp()),
        }
    )
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
