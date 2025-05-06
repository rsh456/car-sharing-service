from starlette import status
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from schemas import UserOutput, User
from db import get_session


URL_PREFIX = "/api/auth"
router = APIRouter(prefix=URL_PREFIX)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URL_PREFIX}/token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)] ,
                    session: Annotated[Session, Depends(get_session)]) -> UserOutput:
    '''
    This function is used to get the current user from the token.
    It uses the OAuth2PasswordBearer to get the token from the request header.
    For this delivery the token will contain only the username
    '''
    query = select(User).where(User.username == token)
    user = session.exec(query).first()
    if user:
        return UserOutput.model_validate(user)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username or password incorrect",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[Session, Depends(get_session)]):
    '''
    This function is used to login the user.
    It uses the OAuth2PasswordRequestForm to get the username and password from the request body.
    '''
    query = select(User).where(User.username == form_data.username)
    user = session.exec(query).first()
    if user and user.verify_password(form_data.password):
        return {"access_token": user.username, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")
    
