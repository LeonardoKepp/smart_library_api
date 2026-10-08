# Usamos Python 3.12 slim para que coincida con tu entorno de desarrollo
FROM python:3.12-slim

WORKDIR /app

# Instalamos las dependencias del sistema necesarias para compilar paquetes de C (como asyncpg y pydantic-core)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto al contenedor
COPY . .

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]