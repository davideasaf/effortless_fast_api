"DB Seession Utils"
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config


# Create SQLAlchemy Engine
engine = create_engine(
    config.DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False}
)

# scoped_session. This is registry of sessions that is thread-local scope.
# Use this outside of a api request session (e.g. doing db work outside of a request)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Session maker. Session() can be called to get a new unique session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
