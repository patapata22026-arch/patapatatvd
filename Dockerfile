# 1. Usar una imagen preconfigurada que YA incluye Python, Chrome estable y Selenium listo
FROM joyzoursbae/python-selenium:latest

# 2. Crear la carpeta de trabajo dentro del servidor virtual
WORKDIR /app

# 3. Copiar los archivos del proyecto al servidor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Comando para arrancar el servidor proxy
CMD ["python", "app.py"]
