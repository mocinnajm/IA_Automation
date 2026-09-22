# 1. Imagen base oficial de Python ligera
FROM python:3.12-slim

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar la lista de dependencias
COPY requirements.txt .

# 4. Instalar las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código del proyecto dentro del contenedor
COPY . .

# 6. Comando por defecto al ejecutar el contenedor (ejecutar las pruebas)
CMD ["pytest", "-v"]
