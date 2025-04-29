from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlmodel import Session, select
from schemas import UserOutput, User
from db import get_session
from starlette import status

security = HTTPBasic()

def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)] ,
                    session: Annotated[Session, Depends(get_session)]) -> UserOutput:
    
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.model_validate(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
        )
