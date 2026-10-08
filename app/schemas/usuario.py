from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
        examples=["Leonardo Kepp"]
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico único del usuario",
        examples=["leonardo@example.com"]
    )
    es_activo: bool = Field(
        default=True,
        description="Estado actual del usuario en el sistema"
    )


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True