# 1. Utilizar la imagen oficial completa de Python para garantizar compatibilidad de librerías
FROM python:3.10

# 2. Instalar Chromium, su driver y las dependencias de fuentes/X11 necesarias para entornos virtuales
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libfontconfig1 \
    x11-common \
    && rm -rf /var/lib/apt/lists/*

# 3. Configurar el directorio de trabajo
WORKDIR /app

# 4. Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código del proyecto
COPY . .

# Definir variables de entorno estables para el sistema
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 6. Comando de arranque
CMD ["python", "app.py"]
