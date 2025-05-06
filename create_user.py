import logging
"""
This script is used to create a new user in the car-sharing application database.
It performs the following tasks:
1. Connects to the SQLite database using SQLModel and creates the necessary tables if they do not exist.
2. Prompts the user to input a username and password securely.
3. Creates a new user instance with the provided username and hashed password.
4. Adds the new user to the database and commits the transaction.
Note:
- Ensure that the `User` schema in the `schemas` module includes a `set_password` method to hash the password.
- The SQLite database file is named `carsharing.db` and is located in the same directory as this script.
"""
from getpass import getpass
from sqlmodel import SQLModel, Session, create_engine
from schemas import User

logging.getLogger('passlib').setLevel(logging.ERROR)

engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},  # Needed for SQLite to work with multiple threads
    echo=True
)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)

    username = input("Please enter username")
    password = getpass("Please enter password")
    with Session(engine) as session:
        user = User(username=username)
        user.set_password(password)
        session.add(user)
        session.commit()