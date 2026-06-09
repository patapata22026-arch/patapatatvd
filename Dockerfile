# 1. Usar una imagen oficial de Python ligera basada en Debian
FROM python:3.11-slim

# 2. Instalar dependencias esenciales de Linux para que corra Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Crear la carpeta de trabajo
WORKDIR /app

# 4. Copiar e instalar librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. Comando de arranque
CMD ["python", "app.py"]
