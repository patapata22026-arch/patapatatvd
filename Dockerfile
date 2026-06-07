# 1. Base oficial liviana
FROM python:3.10-slim

# 2. Instalar Chromium y su driver nativo desde los repositorios de Debian
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 3. Directorio de la app
WORKDIR /app

# 4. Instalar solo Flask y Selenium (pesa muy pocos megabytes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el script
COPY . .

# Variables para fijar las rutas del navegador
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 6. Ejecución
CMD ["python", "app.py"]
