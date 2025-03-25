from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from connections.fmpddbb import SessionLocal
from models.mascota import Mascota
from models.usuario import Usuario, usuario_por_id, id_por_username, propietario_por_id
from models.avistamiento import Avistamiento
from fastapi.templating import Jinja2Templates
from connections import fmpddbb
from security.auth import get_current_user  # Importamos la función para validar el token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/show-pets", response_class=HTMLResponse)
async def show_pets(
    request: Request,
    db: Session = Depends(fmpddbb.get_db)
):
    mascotas_y_dueno = []
    

    lista = db.query(Mascota).all()
    for mascota in lista:
        nombre_usuario = usuario_por_id(db, mascota.id_usuario)
        mascotas_y_dueno.append({
            "nombre": mascota.nombre,
            "tipo": mascota.tipo,
            "color": mascota.color,
            "dueno": nombre_usuario,
            "fecha": mascota.fecha_perdida.strftime("%d/%m/%Y - %H:%M")
        })
    return templates.TemplateResponse("show_pets.html", {"request": request, "lista" : mascotas_y_dueno, "is_authenticated": True})

@router.get("/show-own-pets", response_class=HTMLResponse)
async def show_own_pets(
    request: Request,
    db: Session = Depends(fmpddbb.get_db),
    current_user: str = Depends(get_current_user)
):
    # Verificar si el usuario está autenticado (cookie válida)
    if isinstance(current_user, RedirectResponse):
        return current_user
    
    mascotas = []
    id_user = id_por_username(db, current_user)
    lista = db.query(Mascota).filter(Mascota.id_usuario == id_user)
    for mascota in lista:
        ultimo_avistamiento = db.query(Avistamiento.fecha).filter(Avistamiento.id_mascota == mascota.id).order_by(Avistamiento.fecha.desc()).first()

        mascotas.append({
            "nombre": mascota.nombre,
            "tipo": mascota.tipo,
            "fecha": mascota.fecha_perdida.strftime("%d/%m/%Y - %H:%M"),
            "ultimo_avistamiento": ultimo_avistamiento[0].strftime("%d/%m/%Y - %H:%M") if ultimo_avistamiento else None,
            "id": mascota.id
        })
    return templates.TemplateResponse("show_own_pets.html", {"request": request, "lista" : mascotas})


@router.get("/create-pet", response_class=HTMLResponse)
async def create_pet_form(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(fmpddbb.get_db)

    ):
    if isinstance(current_user, RedirectResponse):
       # Si current_user es una redirección, la devolvemos inmediatamente
       return current_user
    id_usuario = id_por_username(db, current_user)
    if not id_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return templates.TemplateResponse("create_pet.html ", {"request": request, "user_id": id_usuario})


@router.post("/create-pet")
async def create_pet(
    request: Request,
    nombre: str = Form(...),
    tipo: str = Form(...),
    raza: str = Form(...),
    color: str = Form(...),
    db: Session = Depends(fmpddbb.get_db),
    current_user: Usuario = Depends(get_current_user) 
):
    
    if isinstance(current_user, RedirectResponse):
        return current_user
    id_usuario = id_por_username(db, current_user)

    pet = Mascota(
        nombre=nombre,
        tipo=tipo,
        raza=raza,
        color=color,
        id_usuario = id_usuario    
    )

    db.add(pet)
    db.commit()
    db.refresh(pet)
   
    mensaje = "Mascota registrada con éxito."
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

@router.get("/ver-avistamientos/{id_mascota}", response_class=HTMLResponse, name="ver_avistamientos")
async def ver_avistamientos(
    request: Request,
    id_mascota: int,
    db: Session = Depends(fmpddbb.get_db),
    current_user: Usuario = Depends(get_current_user)

):
    # Verificar si el usuario está autenticado (cookie válida)
    if isinstance(current_user, RedirectResponse):
        return current_user

    
    id_usuario = id_por_username(db, current_user)
    mascota = db.query(Mascota).filter(Mascota.id == id_mascota).first()
    data = []

    if not mascota or mascota.id_usuario != id_usuario:
        error = "No tienes esta mascota a tu nombre."

    else:
        avistamientos = db.query(Avistamiento).filter(Avistamiento.id_mascota == id_mascota).all()

        for avist in avistamientos:
            data.append({
                "latitud": avist.latitud,
                "longitud": avist.longitud,
                "fecha": avist.fecha.strftime("%Y-%m-%d %H:%M"),
                "descripcion": avist.descripcion
            })
        if not data:
            error = "No hay avistamientos."
        else: error = None

    return templates.TemplateResponse("mapa_avistamientos.html", {
        "request": request,
        "avistamientos": data,
        "error": error 
    })


@router.post("/eliminar-mascota/{id_mascota}", name="eliminar_mascota")
async def eliminar_mascota(
    request: Request,
    id_mascota: int,
    db: Session = Depends(fmpddbb.get_db),
    current_user: Usuario = Depends(get_current_user)

):
    
    # Verificar si el usuario está autenticado (cookie válida)
    if isinstance(current_user, RedirectResponse):
        return current_user
    
    # Obtener la mascota por ID
    mascota = db.query(Mascota).filter(Mascota.id == id_mascota).first()

    # Verificar si existe
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Verificar si la mascota pertenece al usuario conectado
    id_usuario = id_por_username(db, current_user)
    if mascota.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="No puedes eliminar esta mascota")

    # Eliminar la mascota de la base de datos
    db.delete(mascota)
    db.commit()

    # Redirigir a la lista de mascotas después de eliminar
    return RedirectResponse(url="/show-own-pets", status_code=303)
