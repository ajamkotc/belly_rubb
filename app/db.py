"""
This module sets up the SQLAlchemy database engine and session for the application.

Attributes:
    DB_PATH (str): The database connection string, loaded from the environment variable 'DB_PATH'.
        Defaults to a local SQLite file.
    engine (Engine): The SQLAlchemy engine instance used for database connections.
    Session (sessionmaker): A configured sessionmaker
        bound to the engine for creating database sessions.

Functions:
    init_db():
        Should be called once during application startup to ensure all tables are created.
        Raises SQLAlchemyError if there is an error during table creation.
"""
#pylint: disable=[C0415,W0611]
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

load_dotenv()
DB_PATH = os.getenv(key="DB_PATH", default="sqlite:///bellyrub.db")

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

def init_db():
    """
    Initializes the database by creating all tables defined in the SQLAlchemy Base metadata.

    This function should be called once during application startup to ensure that
    all database tables are created according to the current models.

    Raises:
        SQLAlchemyError: If there is an error during table creation.
    """
    from app.db_models.customer import Customer
    from app.db_models.access_token import AccessToken
    from app.db_models.group import Group
    from app.db_models.group_membership import GroupMembership
    from app.db_models.sync_state import SyncState
    from app.db_models.payment import Payment
    from app.db_models.order import Order

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
