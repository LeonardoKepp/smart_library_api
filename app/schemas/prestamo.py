from pydantic import BaseModel
from datetime import date
from typing import Optional

class PrestamoBase(BaseModel):
    usuario_id: int
    libro_id: int

class PrestamoCreate(PrestamoBase):
    pass 

class PrestamoResponse(PrestamoBase):
    id: int
    fecha_prestamo: date
    fecha_devolucion: date
    estado: str

    class Config:
        from_attributes = True