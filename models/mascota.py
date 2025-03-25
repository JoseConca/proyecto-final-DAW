from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from connections.fmpddbb import Base
from sqlalchemy.orm import Session

from datetime import datetime

class Mascota(Base):
    __tablename__ = "mascota"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    tipo = Column(String, nullable=False)
    raza = Column(String)
    color = Column(String, nullable=False, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_perdida = Column(DateTime, default=datetime.utcnow)
    imagen = Column(String)

def obtener_tipos_de_mascota(db: Session):
    return db.query(Mascota.tipo).distinct().all()

def obtener_colores_por_tipo(db: Session, tipo: str):
    return db.query(Mascota.color).filter(Mascota.tipo == tipo).distinct().all()

def obtener_nombres_por_tipo_y_color(db: Session, tipo: str, color: str):
    return db.query(Mascota.nombre).filter(Mascota.tipo == tipo, Mascota.color == color).distinct().all()

def obtener_id_por_tipo_color_nombre(db: Session, tipo: str, color: str, nombre: str):
    mascota = db.query(Mascota.id).filter(Mascota.tipo == tipo, Mascota.color == color, Mascota.nombre == nombre).first()
    return mascota.id if mascota else None