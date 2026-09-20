import os
import sqlite3
import shutil
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

# -------------------------------------------------------------------
# 1. CONFIGURACIÓN DE REGISTROS (LOGGING)
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
LOG_FILE = os.path.join(PROJECT_DIR, "sistema.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# -------------------------------------------------------------------
# 2. CARGA SEGURA DE VARIABLES DE ENTORNO (.ENV)
# -------------------------------------------------------------------
ENV_PATH = os.path.join(PROJECT_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    mensaje_err = "No se encontró GEMINI_API_KEY en el archivo .env"
    logging.critical(mensaje_err)
    raise ValueError(mensaje_err)

client = genai.Client(api_key=api_key)

# -------------------------------------------------------------------
# 3. RUTAS Y MOLDE DE DATOS (PYDANTIC)
# -------------------------------------------------------------------
CARPETA_ENTRADA = os.path.join(BASE_DIR, "documentos_nuevos")
CARPETA_PROCESADOS = os.path.join(BASE_DIR, "documentos_procesados")
DB_PATH = os.path.join(PROJECT_DIR, "4_Bases_Datos", "subvenciones.db")

class SolicitudSubvencion(BaseModel):
    empresa: str
    presupuesto_solicitado: float
    cumple_requisitos: bool

# -------------------------------------------------------------------
# 4. FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# -------------------------------------------------------------------
def procesar_ficheros():
    logging.info("--- Inicio de procesamiento de lote ---")
    
    os.makedirs(CARPETA_ENTRADA, exist_ok=True)
    os.makedirs(CARPETA_PROCESADOS, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    archivos = [f for f in os.listdir(CARPETA_ENTRADA) if f.endswith('.txt')]
    
    if not archivos:
        print("ℹ️ No hay archivos nuevos para procesar.")
        logging.info("No se encontraron archivos .txt en la carpeta de entrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla con la estructura correcta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT,
            presupuesto REAL,
            cumple_requisitos BOOLEAN,
            estado TEXT
        )
    ''')
    conn.commit()

    for archivo in archivos:
        ruta_archivo = os.path.join(CARPETA_ENTRADA, archivo)
        print(f"📄 Procesando: {archivo}...")
        logging.info(f"Procesando archivo: {archivo}")

        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        prompt = f"""
        Extrae la información relevante de la siguiente solicitud de subvención:
        {contenido}
        """

        intentos = 0
        exito = False

        while intentos < 3 and not exito:
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type='application/json',
                        response_schema=SolicitudSubvencion,
                        temperature=0.1
                    )
                )

                datos = SolicitudSubvencion.model_validate_json(response.text)

                cursor.execute('''
                    INSERT INTO solicitudes (empresa, presupuesto, cumple_requisitos, estado)
                    VALUES (?, ?, ?, 'PENDIENTE')
                ''', (datos.empresa, datos.presupuesto_solicitado, datos.cumple_requisitos))
                
                conn.commit()

                shutil.move(ruta_archivo, os.path.join(CARPETA_PROCESADOS, archivo))
                print(f"✅ Guardado en DB y movido: {archivo}")
                logging.info(f"Éxito al procesar {archivo}. Empresa: {datos.empresa}")
                exito = True

            except Exception as e:
                intentos += 1
                logging.warning(f"Error al procesar {archivo} (Intento {intentos}/3): {e}")
                if intentos < 3:
                    time.sleep(2)
                else:
                    logging.error(f"Fallo definitivo al procesar {archivo} tras 3 intentos.")
                    print(f"❌ Error definitivo con {archivo}. Revisa sistema.log.")

    conn.close()
    logging.info("--- Fin de procesamiento de lote ---")

if __name__ == "__main__":
    procesar_ficheros()
