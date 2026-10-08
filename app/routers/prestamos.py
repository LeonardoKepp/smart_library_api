from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.models.usuario import Usuario
from app.schemas.prestamo import PrestamoCreate, PrestamoResponse

router = APIRouter(
    prefix="/prestamos",
    tags=["Préstamos"]
)

@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
async def crear_prestamo(prestamo: PrestamoCreate, db: AsyncSession = Depends(get_db)):

    resultado_usuario = await db.execute(select(Usuario).where(Usuario.id == prestamo.usuario_id))
    usuario = resultado_usuario.scalar_one_or_none()
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")

    resultado_libro = await db.execute(select(Libro).where(Libro.id == prestamo.libro_id))
    libro = resultado_libro.scalar_one_or_none()
    
    if not libro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe")

    if not libro.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este libro ya está prestado a otro usuario"
        )

    nuevo_prestamo = Prestamo(
        usuario_id=prestamo.usuario_id,
        libro_id=prestamo.libro_id
    )
    db.add(nuevo_prestamo)

    libro.disponible = False

    await db.commit()
    await db.refresh(nuevo_prestamo)
    
    return nuevo_prestamo


@router.get("/", response_model=List[PrestamoResponse])
async def obtener_prestamos(
    usuario_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    estado: Optional[str] = Query(None, description="Filtrar por estado: 'activo' o 'devuelto'"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Prestamo)
    
    if usuario_id:
        query = query.where(Prestamo.usuario_id == usuario_id)
    if estado:
        query = query.where(Prestamo.estado == estado)
        
    resultado = await db.execute(query)
    return resultado.scalars().all()


@router.get("/{prestamo_id}", response_model=PrestamoResponse)
async def obtener_prestamo_por_id(prestamo_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Prestamo).where(Prestamo.id == prestamo_id))
    prestamo = resultado.scalar_one_or_none()
    
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado")
        
    return prestamo


@router.put("/{prestamo_id}/devolver", response_model=PrestamoResponse)
async def devolver_prestamo(prestamo_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Prestamo).where(Prestamo.id == prestamo_id))
    prestamo_db = result.scalars().first()
    
    if not prestamo_db:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
        
    if prestamo_db.estado == "devuelto":
        raise HTTPException(status_code=400, detail="Este préstamo ya ha sido devuelto anteriormente")
        
    prestamo_db.estado = "devuelto"
    
    result_libro = await db.execute(select(Libro).where(Libro.id == prestamo_db.libro_id))
    libro_db = result_libro.scalars().first()
    
    if libro_db:
        libro_db.disponible = True
        
    await db.commit()
    await db.refresh(prestamo_db)
    
    return prestamo_db