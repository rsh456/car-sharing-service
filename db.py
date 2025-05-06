'''
This module contains the database connection and session management for the carsharing application.
It uses SQLModel to interact with a SQLite database.
'''

from sqlmodel import Session
from sqlalchemy import create_engine


engine = create_engine("sqlite:///carsharing.db",
        connect_args={"check_same_thread":False}, # Needed for SQLite to work with multiple threads
        echo=True,) # Remove this in production


def get_session():
    '''
    This function returns a session object that can be used to interact with the database.
    '''
    with Session(engine) as session:
        yield session
