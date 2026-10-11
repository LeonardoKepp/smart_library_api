from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.models.usuario import Usuario
from app.schemas.prestamo import PrestamoCreate, PrestamoResponse
from app.core.security import get_current_user

router = APIRouter(
    prefix="/prestamos",
    tags=["Préstamos"]
)


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
async def crear_prestamo(
    prestamo_datos: PrestamoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    resultado_libro = await db.execute(select(Libro).where(Libro.id == prestamo_datos.libro_id))
    libro = resultado_libro.scalar_one_or_none()

    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {prestamo_datos.libro_id} no fue encontrado"
        )

    if hasattr(libro, "cantidad") and libro.cantidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay copias disponibles de este libro para préstamo"
        )

    nuevo_prestamo = Prestamo(
        usuario_id=current_user.id,
        libro_id=prestamo_datos.libro_id,
        estado="activo"
    )

    if hasattr(libro, "cantidad"):
        libro.cantidad -= 1

    db.add(nuevo_prestamo)
    await db.commit()
    await db.refresh(nuevo_prestamo)
    return nuevo_prestamo


@router.get("/", response_model=List[PrestamoResponse])
async def listar_prestamos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = select(Prestamo).offset(skip).limit(limit)
    resultado = await db.execute(query)
    return resultado.scalars().all()


@router.put("/{prestamo_id}/devolver", response_model=PrestamoResponse)
async def devolver_prestamo(
    prestamo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    resultado = await db.execute(select(Prestamo).where(Prestamo.id == prestamo_id))
    prestamo = resultado.scalar_one_or_none()

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El préstamo con ID {prestamo_id} no fue encontrado"
        )

    if prestamo.estado == "devuelto":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este préstamo ya había sido devuelto anteriormente"
        )

    prestamo.estado = "devuelto"

    resultado_libro = await db.execute(select(Libro).where(Libro.id == prestamo.libro_id))
    libro = resultado_libro.scalar_one_or_none()
    if libro and hasattr(libro, "cantidad"):
        libro.cantidad += 1

    await db.commit()
    await db.refresh(prestamo)
    return prestamo