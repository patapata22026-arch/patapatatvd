# 1. Usar Ubuntu como base estable para asegurar las rutas de Chrome
FROM ubuntu:22.04

# Evitar bloqueos interactivos en la terminal de Render
ENV DEBIAN_FRONTEND=noninteractive

# 2. Instalar Python 3, pip y las dependencias del sistema gráfico elemental
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    librandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 3. Descargar e instalar de forma directa el paquete oficial de Google Chrome Estable
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# 4. Configurar el directorio de la app
WORKDIR /app

# 5. Instalar librerías de Python (Flask y Selenium)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 6. Copiar el código del proyecto
COPY . .

# Comando de arranque explícito para Python 3
CMD ["python3", "app.py"]
