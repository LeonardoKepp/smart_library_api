from sqlalchemy import Column, Integer, Date, ForeignKey, String
from datetime import date, timedelta
from app.database.database import Base

def calcular_fecha_devolucion():
    return date.today() + timedelta(days=14)

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    
    fecha_prestamo = Column(Date, default=date.today, nullable=False)
    fecha_devolucion = Column(Date, default=calcular_fecha_devolucion, nullable=False)
    
    estado = Column(String(20), default="activo", nullable=False)