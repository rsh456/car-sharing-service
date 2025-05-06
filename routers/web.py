'''
This module contains the routes for the web application, 
including the home page and search functionality.
'''

from typing import Annotated, Union
from fastapi import APIRouter, Form, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session
from db import get_session
from routers.cars import get_cars

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)

# The cookie is set in the middleware, but we can also access it here if needed
def home(request: Request, cars_cookie: Annotated[Union[str, None], Cookie()] = None):
    '''
    This function handles the home page of the web application.
    It uses Jinja2 templates to render the HTML page.
    '''
    print(cars_cookie)
    return templates.TemplateResponse(request=request, name="home.html")

@router.post("/search", response_class=HTMLResponse)
def search(size: Annotated[str, Form()],
           doors: Annotated[int, Form()],
           request: Request,
           session: Annotated[Session, Depends(get_session)]) -> HTMLResponse:
    '''
    This function handles the search functionality of the web application.
    '''
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_results.html", {"request": request, "cars": cars})
