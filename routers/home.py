from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from models.usuario import Usuario, id_por_username, usuario_por_id, propietario_por_id
from connections import fmpddbb
from security.auth import get_current_user  # Importamos la función para validar el token

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Session = Depends(fmpddbb.get_db), 
    current_user: str = Depends(get_current_user)
):
    # Verificar si el usuario está autenticado (cookie válida)
    if isinstance(current_user, RedirectResponse):
        response = templates.TemplateResponse("index.html", {
            "request": request,
            "message": "Bienvenido a Find My Pet",
            "is_authenticated": False,     # El usuario no está autenticado
            "is_owner": 0   # 1 si es owner, 0 en caso contrario
    })
    else:
        id_user = id_por_username(db, current_user)
        name = usuario_por_id(db, id_user)
        user_owner = propietario_por_id(db, id_user)
        # Renderizar la plantilla con las variables necesarias
        response = templates.TemplateResponse("index.html", {
            "request": request,
            "message": "Bienvenido a Find My Pet",
            "user": name,
            "is_authenticated": True,     # El usuario está autenticado
            "is_owner": user_owner   # 1 si es owner, 0 en caso contrario
        })
    
    return response