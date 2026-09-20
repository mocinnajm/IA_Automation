# Apuntes de Automatización e IA

## 1. Comandos del Entorno y Acceso Rápido
- Acceso directo configurado: `ir_ia` (entra a la carpeta y activa el entorno `env_gemini`).
- Ejecución con Python del entorno: `~/IA_Automation/env_gemini/bin/python3 script.py`

## 2. Puntos Clave de la API de Gemini
- **Modelo actual (2026):** `gemini-3.6-flash`
- **Extracción limpia:** Usar `response_mime_type="application/json"` y esquemas con `Pydantic`.
- **Manejo de Errores (El Paracaídas):**
  - Error `404 NOT_FOUND`: El modelo no existe o está mal escrito.
  - Error `503 UNAVAILABLE`: Sobrecarga temporal. Se soluciona con `try / except` y reintentos con `time.sleep()`.

## 3. Consultas Rápidas de SQLite en Terminal
- Ver todos los registros: `sqlite3 ~/IA_Automation/4_Bases_Datos/subvenciones.db "SELECT * FROM solicitudes;"`
- Actualizar estado: `sqlite3 ~/IA_Automation/4_Bases_Datos/subvenciones.db "UPDATE solicitudes SET estado='APROBADO' WHERE id=1;"`

## 4. Esquema de Procesamiento en Lote (`procesar_lote.py`)
> **Frase Feynman:** *`procesar_lote.py` es una cinta transportadora que lee cartas de una bandeja, usa la IA para rellenar un formulario limpio, guarda el resultado en un archivador SQL y mueve la carta leída a otra carpeta.*

### Los 5 Pasos del Bucle:
1. **El Recepcionista (Lectura):** Lee los archivos `.txt` pendientes en `documentos_nuevos`.
2. **El Traductor (Gemini + Pydantic):** Extrae los datos obligando a la IA a rellenar la ficha limpia (JSON).
3. **El Paracaídas (`try / except`):** Si responde con error `503`, espera unos segundos y reintenta.
4. **El Archivador (SQLite):** Guarda la solicitud con su estado inicial `PENDIENTE` en `subvenciones.db`.
5. **El Limpiador (`shutil.move`):** Traslada el archivo a `documentos_procesados`.

## 5. El Inspector de Calidad (`evaluar_solicitudes.py`)
> **Frase Feynman:** *El Inspector no lee documentos ni usa la IA; va directo a la base de datos a revisar registros PENDIENTES y les aplica las reglas del negocio.*

### Reglas de Negocio Aplicadas:
1. **Presupuesto <= 30.000 €:** Cambia el estado a **`APROBADO`**.
2. **Presupuesto > 30.000 €:** Cambia el estado a **`RECHAZADO`**.

### Consulta SQL utilizada (UPDATE):
`UPDATE solicitudes SET estado = ? WHERE id = ?;`

---

## 6. Seguridad con `.env` (`python-dotenv`)
> **Frase Feynman:** *El archivo `.env` es la libreta secreta de claves. Python usa `load_dotenv()` para leer la clave sin escribirla dentro del código.*

### Pasos:
1. Crear el archivo `.env`: `GEMINI_API_KEY=tu_clave`
2. En Python: `load_dotenv()` y `os.getenv("GEMINI_API_KEY")`.

---

## 7. Registro de Errores Profesional (`logging`)
> **Frase Feynman:** *`print()` habla para la pantalla; `logging` escribe en el libro de diario para revisar los errores en el futuro.*

### Configuración básica:
- **logging.info()**: Para registrar mensajes de confirmación o inicio.
- **logging.error()**: Para guardar fallos capturados en bloques try / except.

