import os
import sqlite3
import logging

# -------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LOGGING
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

DB_PATH = os.path.join(PROJECT_DIR, "4_Bases_Datos", "subvenciones.db")

# -------------------------------------------------------------------
# 2. EVALUACIÓN DE REGLAS DE NEGOCIO
# -------------------------------------------------------------------
def evaluar_pendientes():
    logging.info("--- Inicio de evaluación de reglas de negocio ---")
    
    if not os.path.exists(DB_PATH):
        print("❌ No existe la base de datos.")
        logging.warning("Intento de evaluación sin base de datos existente.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Buscar registros en estado PENDIENTE
    cursor.execute("SELECT id, empresa, presupuesto, cumple_requisitos FROM solicitudes WHERE estado = 'PENDIENTE'")
    pendientes = cursor.fetchall()

    if not pendientes:
        print("ℹ️ No hay solicitudes pendientes de evaluación.")
        logging.info("Evaluación finalizada: 0 solicitudes pendientes.")
        conn.close()
        return

    print(f"🔍 Evaluando {len(pendientes)} solicitud(es)...")

    for sol in pendientes:
        id_sol, empresa, presupuesto, cumple_req = sol
        
        # Regla de negocio: Cumplir requisitos y presupuesto <= 50,000 EUR
        if cumple_req and presupuesto <= 50000.0:
            nuevo_estado = "APROBADA"
        else:
            nuevo_estado = "RECHAZADA"

        cursor.execute("UPDATE solicitudes SET estado = ? WHERE id = ?", (nuevo_estado, id_sol))
        print(f"📋 Solicitud #{id_sol} ({empresa}): {nuevo_estado}")
        logging.info(f"Solicitud #{id_sol} de '{empresa}' evaluada -> {nuevo_estado}")

    conn.commit()
    conn.close()
    logging.info("--- Fin de evaluación de reglas de negocio ---")

if __name__ == "__main__":
    evaluar_pendientes()
