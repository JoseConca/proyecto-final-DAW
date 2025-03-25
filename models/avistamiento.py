from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from connections.fmpddbb import Base

class Avistamiento(Base):
    __tablename__ = "avistamiento"
    
    id = Column(Integer, primary_key=True, index=True)
    latitud = Column(String, nullable=False)
    longitud = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_mascota = Column(Integer, ForeignKey("mascota.id"), nullable=False)
