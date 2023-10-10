from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# The engine represents the database connection. It manages the connection pool and communicates with the database server.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# The sessionmaker() function is used to create a session factory.
# The session factory generates individual session objects that provide a context for database operations.
# In the example, SessionLocal is created by calling sessionmaker() and passing the engine as the bind parameter.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class of ORM models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
