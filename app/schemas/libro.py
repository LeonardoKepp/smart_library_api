from pydantic import BaseModel, Field


class LibroBase(BaseModel):
    titulo: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Título del libro (1 a 150 caracteres)",
        examples=["All Tomorrows"]
    )
    autor: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del autor (1 a 100 caracteres)",
        examples=["C.M. Kosemen"]
    )
    anio_publicacion: int = Field(
        ...,
        ge=1000,
        le=2026,
        description="Año de publicación (debe ser un año entre 1000 y 2026)",
        examples=[2004]
    )
    disponible: bool = Field(
        default=True,
        description="Indica si el libro está disponible para préstamo"
    )


class LibroCreate(LibroBase):
    pass


class LibroResponse(LibroBase):
    id: int

    class Config:
        from_attributes = True