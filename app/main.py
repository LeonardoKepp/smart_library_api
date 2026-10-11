import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.database.database import engine, Base
from app.routers.libros import router as libros_router
from app.routers.usuarios import router as usuarios_router
from app.routers.prestamos import router as prestamos_router
from app.routers.auth import router as auth_router  
from app.models import libro, usuario, prestamo

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 5
    retry_delay = 3
    
    for attempt in range(1, max_retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("¡Conexión a la base de datos establecida y tablas creadas exitosamente!")
            break
        except OperationalError as e:
            if attempt == max_retries:
                logger.error("Se agotaron los intentos de conexión a la base de datos.")
                raise e
            logger.warning(f"Intento {attempt}/{max_retries}: Base de datos no disponible todavía. Reintentando en {retry_delay} segundos...")
            await asyncio.sleep(retry_delay)
            
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Biblioteca Inteligente",
        description="API REST desarrollada con FastAPI, SQLAlchemy y PostgreSQL para la gestión de libros, usuarios y préstamos.",
        version="1.0.0",
        lifespan=lifespan
    )

    app.include_router(libros_router)
    app.include_router(usuarios_router)
    app.include_router(prestamos_router)
    app.include_router(auth_router)  

    @app.get("/")
    async def inicio():
        return {"mensaje": "Bienvenido a la API de la Biblioteca Inteligente - UNET"}

    return app

app = create_app()