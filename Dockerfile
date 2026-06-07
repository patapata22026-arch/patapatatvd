# 1. Base limpia y oficial de Python
FROM python:3.10-slim

# 2. Instalar Chromium y su driver nativo de forma directa
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 3. Configurar directorio de trabajo
WORKDIR /app

# 4. Instalar librerías básicas de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código del proxy
COPY . .

# Comando de ejecución seguro
CMD ["python", "app.py"]
