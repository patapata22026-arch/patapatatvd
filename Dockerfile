# 1. Usar una imagen oficial optimizada que YA tiene Chrome instalado de fábrica
FROM selenium/standalone-chrome:latest

# Cambiar temporalmente a usuario root para instalar dependencias de Python
USER root

# 2. Instalar Python pip (esta imagen ya trae Python integrado)
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

# 3. Configurar directorio de la aplicación
WORKDIR /app

# 4. Copiar e instalar librerías de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Copiar el script del proxy
COPY . .

# Volver a usuario seguro por políticas de Render
USER seluser

# 6. Comando de arranque explícito
CMD ["python3", "app.py"]
