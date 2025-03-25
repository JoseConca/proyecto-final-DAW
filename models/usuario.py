from sqlalchemy import Column, Integer, String, Boolean, DateTime, select
from sqlalchemy.orm import Session

from datetime import datetime
from connections.fmpddbb import Base

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    insc_date = Column(DateTime, default=datetime.utcnow)
    email = Column(String, unique=True, nullable=False)
    owner = Column(Boolean, default=False)

def usuario_por_id(db: Session, id: int) -> str:
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario:
        return usuario.name
    return "Usuario no encontrado"

def id_por_username(db: Session, username: str) -> int:
    return db.query(Usuario).filter(Usuario.username == username).first().id

def propietario_por_id(db: Session, id: int) -> str:
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario:
        return usuario.owner
    return "Usuario no encontrado"
