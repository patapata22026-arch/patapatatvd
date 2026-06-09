# 1. Usar una imagen oficial de Python basada en Linux
FROM python:3.11-slim

# 2. Instalar Google Chrome y dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/組織/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. Crear carpeta de trabajo dentro del servidor
WORKDIR /app

# 4. Copiar e instalar las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código al servidor
COPY . .

# 6. Comando para arrancar nuestra aplicación de Flask
CMD ["python", "app.py"]
