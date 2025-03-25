from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from connections.fmpddbb import get_db
from models.avistamiento import Avistamiento
from models.usuario import Usuario
from models.mascota import Mascota, obtener_colores_por_tipo, obtener_id_por_tipo_color_nombre, obtener_nombres_por_tipo_y_color, obtener_tipos_de_mascota
from security.auth import get_current_user
from models.usuario import Usuario, id_por_username, usuario_por_id, propietario_por_id
from datetime import datetime
from connections import fmpddbb

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/avistamiento", response_class=HTMLResponse)
async def registrar_avistamiento(request: Request, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    
    tipos = obtener_tipos_de_mascota(db)
    return templates.TemplateResponse("avistamiento.html", {"request": request, "user": current_user, "tipos": [tipo[0] for tipo in tipos]})

@router.post("/avistamiento", response_class=HTMLResponse)
async def registrar_avistamiento_post(
    request: Request,
    latitud: str = Form(...),
    longitud: str = Form(...),
    descripcion: str = Form(...),
    id_mascota: int = Form(...), 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user
    id_usuario = id_por_username(db, current_user)


    # Crear y almacenar el nuevo avistamiento en la base de datos
    nuevo_avistamiento = Avistamiento(
        latitud=latitud,
        longitud=longitud,
        descripcion=descripcion,
        fecha=datetime.utcnow(),
        id_usuario=id_usuario,
        id_mascota=id_mascota  #Probando ..
    )
    
    db.add(nuevo_avistamiento)
    db.commit()
    db.refresh(nuevo_avistamiento)


    mensaje = "Avistamiento registrado con éxito."

    id_user = id_por_username(db, current_user)
    name = usuario_por_id(db, id_user)
    user_owner = propietario_por_id(db, id_user)
    response = templates.TemplateResponse("index.html", {
            "request": request,
            "message": mensaje,
            "user": name,
            "is_authenticated": True,     # El usuario está autenticado
            "is_owner": user_owner   # 1 si es owner, 0 en caso contrario
        })
    
    return response

#Llamadas del js para coger info de la bbdd
@router.get("/api/colores")
async def obtener_colores(tipo: str, db: Session = Depends(get_db)):
    colores = obtener_colores_por_tipo(db, tipo)
    return {"colores": [color[0] for color in colores]}  # Extrae solo los valores

@router.get("/api/mascotas")
async def obtener_mascotas(tipo: str, color: str, db: Session = Depends(get_db)):
    nombres = obtener_nombres_por_tipo_y_color(db, tipo, color)
    mascotas = [{"id": obtener_id_por_tipo_color_nombre(db, tipo, color, nombre[0]), "nombre": nombre[0]} for nombre in nombres]
    return {"mascotas": mascotas}
