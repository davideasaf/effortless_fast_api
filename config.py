"config"

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy Connection string
# use provided ENV variable connection string
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", f"sqlite:////{BASEDIR}/effortless-fast-dev.db"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
SECRET_KEY = "my-super-secret-dev-key"
