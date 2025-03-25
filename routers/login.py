from fastapi.security import OAuth2PasswordRequestForm
from security.auth import create_access_token, verify_password
from fastapi import HTTPException, status, Depends, APIRouter, Request, Response
from models.usuario import Usuario
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from fastapi.responses import HTMLResponse, RedirectResponse
from connections import fmpddbb

router = APIRouter()
templates = Jinja2Templates(directory="templates")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, response: Response, db: Session = Depends(fmpddbb.get_db), 
                form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    # Verificación de usuario y contraseña
    if not user or not verify_password(form_data.password, user.password):
        error_message = "Usuario o contraseña incorrectos."
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

    # Generar token de acceso
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Redirigir a la página principal con el token guardado en una cookie
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response


@router.get("/logout")
async def logout(request: Request):
    # Eliminar la cookie access_token
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")  # Eliminar la cookie
    return response