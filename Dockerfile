# 1. Usar la imagen OFICIAL de Selenium con Chrome e idioma Python integrado
FROM selenium/standalone-chrome:latest

# Instalar Python pip dentro de la imagen de Selenium de forma segura
USER root
RUN apt-get update && apt-get install -y python3-pip python3-venv && rm -rf /var/lib/apt/lists/*
USER seluser

# 2. Crear la carpeta de trabajo
WORKDIR /app

# 3. Copiar e instalar las librerías de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

# 4. Comando para arrancar el servidor proxy
CMD ["python3", "app.py"]
