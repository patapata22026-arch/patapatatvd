# Usar una imagen preconfigurada que YA incluye Python y Chrome estable listo para usar
FROM joyzoursbae/python-selenium:latest

# Crear la carpeta de trabajo dentro del servidor virtual
WORKDIR /app

# Copiar los archivos de los requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de tu proyecto
COPY . .

# Comando para arrancar tu proxy
CMD ["python", "app.py"]
