import sqlite3
import os
import sys

# 1. Configurar ruta para importar notificador.py desde la raíz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(ROOT_DIR)

from notificador import enviar_notificacion_telegram

# 2. Ruta a la base de datos
DB_PATH = os.path.join(BASE_DIR, "../4_Bases_Datos/subvenciones.db")

print("--- 🔍 INSPECTOR DE CALIDAD: Evaluando Solicitudes ---")

# 3. Conexión a SQLite
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# 4. Buscar solicitudes pendientes
query_pendientes = "SELECT id, empresa, presupuesto FROM solicitudes WHERE estado = 'PENDIENTE';"
cursor.execute(query_pendientes)
pendientes = cursor.fetchall()

if not pendientes:
    print("ℹ️ No hay solicitudes pendientes por evaluar.")
    conexion.close()
    sys.exit()

print(f"📋 Se han encontrado {len(pendientes)} solicitudes pendientes por revisar.\n")

# 5. Evaluar cada solicitud y notificar por Telegram
APROBADOS_COUNT = 0
RECHAZADOS_COUNT = 0

for ficha in pendientes:
    id_solicitud = ficha[0]
    nombre_empresa = ficha[1]
    presupuesto = ficha[2]

    # Aplicación de Reglas de Negocio
    if presupuesto <= 30000.0:
        nuevo_estado = "APROBADO"
        APROBADOS_COUNT += 1
        motivo = f"Presupuesto aceptado ({presupuesto} € <= 30000 €)"
        emoji = "✅"
    else:
        nuevo_estado = "RECHAZADO"
        RECHAZADOS_COUNT += 1
        motivo = f"Presupuesto excede el límite ({presupuesto} € > 30000 €)"
        emoji = "❌"

    # Actualizar estado en la Base de Datos
    cursor.execute(
        "UPDATE solicitudes SET estado = ? WHERE id = ?;",
        (nuevo_estado, id_solicitud)
    )

    # Construir y enviar mensaje a Telegram
    mensaje = (
        f"🤖 *Inspector IA - Solicitud Procesada*\n\n"
        f"🏢 *Empresa:* {nombre_empresa}\n"
        f"💶 *Presupuesto:* {presupuesto} €\n"
        f"{emoji} *Estado:* {nuevo_estado}\n"
        f"ℹ️ *Motivo:* {motivo}"
    )
    enviar_notificacion_telegram(mensaje)
    print(f"-> {nombre_empresa}: {nuevo_estado} (Notificación enviada)")

# Guardar cambios en la base de datos
conexion.commit()
conexion.close()

print(f"\n✅ Proceso finalizado. Aprobados: {APROBADOS_COUNT} | Rechazados: {RECHAZADOS_COUNT}")
