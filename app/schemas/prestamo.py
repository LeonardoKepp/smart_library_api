from pydantic import BaseModel, Field
from datetime import datetime

class PrestamoBase(BaseModel):
    libro_id: int = Field(..., description="ID del libro que se desea solicitar")

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoResponse(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    estado: str

    class Config:
        from_attributes = True