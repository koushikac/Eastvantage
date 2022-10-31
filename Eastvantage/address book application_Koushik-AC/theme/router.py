from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags=['Themes'],
    prefix='/themes'
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def show_theme(request: Request):

    return templates.TemplateResponse("home.html", {"request": request})


