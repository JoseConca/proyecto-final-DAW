from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from connections.fmpddbb import SessionLocal
from models.usuario import Usuario
from security import auth
from fastapi.templating import Jinja2Templates
from connections import fmpddbb
from security.auth import get_current_user  # Importamos la función para validar el token


router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
#Código para facilitar la depuración
@router.get("/show-users", response_class=HTMLResponse)
async def show_users(
    request: Request,
    db: Session = Depends(fmpddbb.get_db),
    #Validar autenticación
    current_user: str = Depends(get_current_user)
):  
    if isinstance(current_user, RedirectResponse):
       # Si current_user es una redirección, la devolvemos inmediatamente
       return current_user

    lista = db.query(Usuario).all()
    return templates.TemplateResponse("show_users.html", {"request": request, "lista" : lista, "user" : current_user})
"""
@router.get("/create-user", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html ", {"request": request})

@router.post("/create-user")
async def create_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    email: str = Form(...),
    owner: bool = Form(False),
    db: Session = Depends(fmpddbb.get_db)
):
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(Usuario.username == username).first()
    if existing_user:
        response = templates.TemplateResponse("create_user.html", {
            "request": request,
            "message": "Este usuario ya existe",
        })
        return response

    #encriptamos la contraseña
    hashed_password = auth.hash_password(password)
    user = Usuario(
        username=username,
        password=hashed_password,
        name=name,
        age=age,
        email=email,
        owner=owner
    )
    print(user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/", status_code=303)
