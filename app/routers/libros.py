from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.models.libro import Libro
from app.schemas.libro import LibroCreate, LibroResponse

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)


@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
async def crear_libro(libro: LibroCreate, db: AsyncSession = Depends(get_db)):
    nuevo_libro = Libro(**libro.model_dump())
    db.add(nuevo_libro)
    await db.commit()
    await db.refresh(nuevo_libro)
    return nuevo_libro


@router.get("/", response_model=List[LibroResponse])
async def obtener_libros(
    titulo: Optional[str] = Query(None, description="Búsqueda parcial por título (ej. 'Tomorrows')"),
    autor: Optional[str] = Query(None, description="Búsqueda parcial por autor (ej. 'Kosemen')"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad (true/false)"),
    skip: int = Query(0, ge=0, description="Cantidad de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de registros a devolver"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Libro)

    if titulo:
        query = query.where(Libro.titulo.ilike(f"%{titulo}%"))
    if autor:
        query = query.where(Libro.autor.ilike(f"%{autor}%"))
    if disponible is not None:
        query = query.where(Libro.disponible == disponible)

    query = query.offset(skip).limit(limit)

    resultado = await db.execute(query)
    libros = resultado.scalars().all()
    return libros

@router.get("/{libro_id}", response_model=LibroResponse)
async def obtener_libro_por_id(libro_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Libro).where(Libro.id == libro_id))
    libro = resultado.scalar_one_or_none()
    
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {libro_id} no fue encontrado"
        )
    return libro

@router.put("/{libro_id}", response_model=LibroResponse)
async def actualizar_libro(
    libro_id: int, 
    libro_datos: LibroCreate, 
    db: AsyncSession = Depends(get_db)
):
    resultado = await db.execute(select(Libro).where(Libro.id == libro_id))
    libro = resultado.scalar_one_or_none()
    
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {libro_id} no existe para ser actualizado"
        )
    
    for campo, valor in libro_datos.model_dump().items():
        setattr(libro, campo, valor)
        
    await db.commit()
    await db.refresh(libro)
    return libro

@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_libro(libro_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Libro).where(Libro.id == libro_id))
    libro = resultado.scalar_one_or_none()
    
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El libro con ID {libro_id} no existe"
        )
    
    await db.delete(libro)
    await db.commit()
    return None