from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean
from app.database.database import Base

class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    autor: Mapped[str] = mapped_column(String(100), nullable=False)
    anio_publicacion: Mapped[int] = mapped_column(Integer, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)