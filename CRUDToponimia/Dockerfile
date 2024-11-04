# Dockerfile
# Usa una imagen oficial de Python
FROM python:3.12

# Configura el directorio de trabajo en el contenedor
WORKDIR /app/CRUDToponimia

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto Django en el contenedor
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

