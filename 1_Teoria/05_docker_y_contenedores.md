# 🐳 APUNTES DE TEORÍA: DOCKER Y CONTENERIZACIÓN

---

## 🧠 1. Conceptos Clave para Respuestas en Entrevistas

* **Contenedor:** Entorno aislado que empaqueta el código, las dependencias y la configuración necesaria para ejecutar una aplicación.
* **Imagen Docker:** Plantilla ejecutable de solo lectura que contiene las instrucciones para crear un contenedor.
* **Dockerfile:** Archivo de texto sin extensión que contiene la "receta" paso a paso para construir una imagen Docker.
* **Docker Compose:** Herramienta para definir y ejecutar aplicaciones compuestas por múltiples contenedores en un solo archivo (`docker-compose.yml`).

---

## 💡 2. Frases Listas para Memorizar (Para la Entrevista)

* **¿Por qué utilizas Docker en tus proyectos?**
  > "Para evitar el problema de 'funciona en mi máquina pero no en el servidor'. Docker empaqueta el entorno exacto, garantizando portabilidad entre local, staging y producción."
* **¿Qué diferencia hay entre una Imagen y un Contenedor?**
  > "La Imagen es la receta (el plano estático) y el Contenedor es la instancia en ejecución (el plato servido)."
* **¿Qué pasos sigues para empaquetar una aplicación Python?**
  > "Defino una imagen base (ej. `python:3.12-slim`), copio el `requirements.txt`, instalo las dependencias, copio el código y defino el comando de entrada (`CMD`)."

---

## 💻 3. Comandos Esenciales de Terminal

* `docker build -t mi-app .` -> Construye la imagen a partir del Dockerfile actual.
* `docker run mi-app` -> Arranca un contenedor basado en esa imagen.
* `docker ps` -> Muestra los contenedores que están actualmente en ejecución.
* `docker images` -> Lista las imágenes creadas en tu sistema.
---

## 🛠️ Comandos de uso práctico habitual

* `docker build -t ia-automation-app .` -> Construye la imagen leyendo el Dockerfile.
* `docker run --rm ia-automation-app` -> Ejecuta los tests en un contenedor temporal y lo elimina al terminar.
