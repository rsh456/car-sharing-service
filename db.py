from sqlmodel import Session
from sqlalchemy import create_engine


engine = create_engine("sqlite:///carsharing.db",
        connect_args={"check_same_thread":False}, # Needed for SQLite to work with multiple threads
        echo=True,) # Remove this in production
## Define a method to return the session
def get_session():
    with Session(engine) as session:
        yield session
