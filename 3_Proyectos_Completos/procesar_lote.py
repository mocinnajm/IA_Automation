import os
import time
import shutil
import sqlite3
import logging
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# -------------------------------------------------------------------
# 1. CONFIGURACIÓN DE ENTORNO Y LOGGING
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

load_dotenv(os.path.join(PROJECT_DIR, ".env"))

LOG_FILE = os.path.join(PROJECT_DIR, "sistema.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logging.critical("No se encontró la GEMINI_API_KEY en el archivo .env")
    raise ValueError("Error: GEMINI_API_KEY no configurada.")

client = genai.Client(api_key=API_KEY)

DIR_ENTRADA = os.path.join(BASE_DIR, "documentos_nuevos")
DIR_PROCESADOS = os.path.join(BASE_DIR, "documentos_procesados")
DB_PATH = os.path.join(PROJECT_DIR, "4_Bases_Datos", "subvenciones.db")

for directorio in [DIR_ENTRADA, DIR_PROCESADOS, os.path.dirname(DB_PATH)]:
    os.makedirs(directorio, exist_ok=True)

# -------------------------------------------------------------------
# 2. ESQUEMA PYDANTIC
# -------------------------------------------------------------------
class SolicitudSubvencion(BaseModel):
    empresa: str = Field(description="Nombre oficial de la empresa solicitante")
    cif: str = Field(description="CIF o NIF de la empresa")
    presupuesto: float = Field(description="Presupuesto solicitado en euros")
    cumple_requisitos: bool = Field(description="True si cumple todos los requisitos explícitos, False en caso contrario")

# -------------------------------------------------------------------
# 3. BASE DE DATOS
# -------------------------------------------------------------------
def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            cif TEXT NOT NULL,
            presupuesto REAL NOT NULL,
            cumple_requisitos BOOLEAN NOT NULL,
            estado TEXT DEFAULT 'PENDIENTE',
            fecha_procesado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def guardar_solicitud(datos: SolicitudSubvencion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO solicitudes (empresa, cif, presupuesto, cumple_requisitos, estado)
        VALUES (?, ?, ?, ?, 'PENDIENTE')
    ''', (datos.empresa, datos.cif, datos.presupuesto, datos.cumple_requisitos))
    conn.commit()
    conn.close()

# -------------------------------------------------------------------
# 4. EXTRACCIÓN MULTIMODAL CON GEMINI
# -------------------------------------------------------------------
def extraer_datos_con_gemini(ruta_archivo: str) -> SolicitudSubvencion:
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    prompt = (
        "Extrae la información relevante de esta solicitud de subvención. "
        "Determina si la empresa cumple con los requisitos mínimos según el texto o documento suministrado."
    )

    contents = []

    if extension == ".pdf":
        # Carga el archivo PDF usando la Files API de Gemini para procesamiento multimodal
        file_ref = client.files.upload(file=ruta_archivo)
        contents = [file_ref, prompt]
    else:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            texto_documento = f.read()
        contents = [f"{prompt}\n\nTexto del documento:\n{texto_documento}"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SolicitudSubvencion,
            temperature=0.1
        )
    )
    
    # Si se subió un PDF a la Files API, procedemos a limpiarlo
    if extension == ".pdf":
        try:
            client.files.delete(name=file_ref.name)
        except Exception as e:
            logging.warning(f"No se pudo eliminar el archivo temporal en Gemini Files: {e}")

    return SolicitudSubvencion.model_validate_json(response.text)

# -------------------------------------------------------------------
# 5. PIPELINE PRINCIPAL
# -------------------------------------------------------------------
def procesar_lote():
    logging.info("--- Inicio de procesamiento de lote ---")
    inicializar_bd()

    archivos = [
        f for f in os.listdir(DIR_ENTRADA) 
        if f.lower().endswith(('.txt', '.pdf')) and not f.startswith('.')
    ]

    if not archivos:
        print("ℹ️ No hay documentos (.txt o .pdf) pendientes en la carpeta de entrada.")
        logging.info("Procesamiento finalizado: 0 archivos encontrados.")
        return

    print(f"📄 Se encontraron {len(archivos)} archivo(s) para procesar.")

    for archivo in archivos:
        ruta_origen = os.path.join(DIR_ENTRADA, archivo)
        print(f"\n🔄 Procesando: {archivo}...")

        exito = False
        for intento in range(1, 4):
            try:
                datos = extraer_datos_con_gemini(ruta_origen)
                guardar_solicitud(datos)
                
                ruta_destino = os.path.join(DIR_PROCESADOS, archivo)
                shutil.move(ruta_origen, ruta_destino)
                
                print(f"✅ Éxito: {datos.empresa} - {datos.presupuesto:,.2f} EUR (Intento {intento})")
                logging.info(f"Archivo '{archivo}' procesado correctamente -> Empresa: {datos.empresa}")
                exito = True
                break

            except Exception as e:
                logging.warning(f"Intento {intento} fallido para '{archivo}': {e}")
                print(f"⚠️ Error en intento {intento}: {e}")
                time.sleep(2)

        if not exito:
            logging.error(f"El archivo '{archivo}' no se pudo procesar tras 3 intentos.")
            print(f"❌ Falló el procesamiento de '{archivo}'. Se mantendrá en entrada para revisión.")

    logging.info("--- Fin de procesamiento de lote ---")

if __name__ == "__main__":
    procesar_lote()
