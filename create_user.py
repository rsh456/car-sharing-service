import logging
from getpass import getpass
from sqlmodel import SQLModel, Session, create_engine
from schemas import User

logging.getLogger('passlib').setLevel(logging.ERROR)

engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},  # Needed for SQLite to work with multiple threads
    echo=True, 
)

if __name__ == "__main__":
    print("Create tables if necessary")
    SQLModel.metadata.create_all(engine)

    username = input("Please enter username")
    password = getpass("Please enter password")
    with Session(engine) as session:
        user = User(username=username)
        user.set_password(password)
        session.add(user)
        session.commit()