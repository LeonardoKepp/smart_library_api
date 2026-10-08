from pydantic import BaseModel
from datetime import date
from typing import Optional

# 1. Esquema Base: Lo que es común en todas las peticiones
class PrestamoBase(BaseModel):
    usuario_id: int
    libro_id: int

# 2. Esquema para Crear (Lo que el cliente nos envía)
class PrestamoCreate(PrestamoBase):
    pass # No necesitamos pedirle fechas al usuario, la base de datos las calcula solas

# 3. Esquema de Respuesta (Lo que la API le devuelve al cliente)
class PrestamoResponse(PrestamoBase):
    id: int
    fecha_prestamo: date
    fecha_devolucion: date
    estado: str

    # Esta configuración permite que Pydantic lea los datos de SQLAlchemy
    class Config:
        from_attributes = True