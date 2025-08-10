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
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_models import Base

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
    Base.metadata.create_all(engine)
