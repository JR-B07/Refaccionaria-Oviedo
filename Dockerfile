# Dockerfile para app Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY REFACCIONARIA/ .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto (ajusta si usas otro)
EXPOSE 8000

# Comando para iniciar la app
CMD ["python", "start.py"]
