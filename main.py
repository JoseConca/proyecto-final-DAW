from fastapi import FastAPI

#Servicios web asíncronos
from starlette.staticfiles import StaticFiles

from connections.fmpddbb import Base, engine
from routers import home, users, mascotas, login, avistamiento
#Seguridad
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir el router para las rutas de la aplicación

app.include_router(login.router)
app.include_router(home.router)
app.include_router(users.router)
app.include_router(mascotas.router)
app.include_router(avistamiento.router)

# Montar la carpeta "static" en "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")