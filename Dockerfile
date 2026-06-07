# 1. Usar una imagen oficial de Ubuntu estable y moderna
FROM ubuntu:22.04

# Evitar que Linux se quede esperando respuestas interactivas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# 2. Instalar Python, herramientas de red y las librerías necesarias para Chrome
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    curl \
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
    && rm -rf /var/lib/apt/lists/*

# 3. Instalar Google Chrome usando el método moderno compatible con servidores en la nube
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/googlechrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 4. Configurar la carpeta del proyecto
WORKDIR /app

# Copiar requerimientos e instalar paquetes de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# 5. Comando para arrancar el proxy usando Python 3
CMD ["python3", "app.py"]
