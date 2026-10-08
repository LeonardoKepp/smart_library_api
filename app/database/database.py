import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# URL de conexión para PostgreSQL usando asyncpg (puerto 5432 del contenedor)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://admin_library:secure_password_unet@localhost:5432/smart_library_db"
)

# Motor asíncrono de SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Fábrica de sesiones para las peticiones de la API
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base declarativa para nuestros modelos ORM
class Base(DeclarativeBase):
    pass

# Dependencia de FastAPI para obtener la sesión de base de datos por cada request
async def get_db():
    async with SessionLocal() as session:
        yield session