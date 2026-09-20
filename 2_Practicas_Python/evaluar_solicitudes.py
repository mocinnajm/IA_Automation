import sqlite3
import os

# 1. Localizar la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../4_Bases_Datos/subvenciones.db")

print("--- 🔍 INSPECTOR DE CALIDAD: Evaluando Solicitudes ---")

# 2. Abrir el archivador (Conexión a SQLite)
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# 3. Buscar SOLO las fichas con estado 'PENDIENTE'
query_pendientes = "SELECT id, empresa, presupuesto FROM solicitudes WHERE estado = 'PENDIENTE';"
cursor.execute(query_pendientes)
pendientes = cursor.fetchall()

if not pendientes:
    print("ℹ️ No hay solicitudes pendientes por evaluar.")
    conexion.close()
    exit()

print(f"📋 Se han encontrado {len(pendientes)} solicitudes pendientes por revisar.\n")

# 4. Bucle para revisar cada ficha (Aplicar las Reglas)
APROBADOS_COUNT = 0
RECHAZADOS_COUNT = 0

for ficha in pendientes:
    id_solicitud = ficha[0]
    nombre_empresa = ficha[1]
    presupuesto = ficha[2]

    # APLICACIÓN DE LAS REGLAS DE NEGOCIO
    if presupuesto <= 30000.0:
        nuevo_estado = "APROBADO"
        APROBADOS_COUNT += 1
        motivo = f"Presupuesto aceptado ({presupuesto} € <= 30000 €)"
    else:
        nuevo_estado = "RECHAZADO"
        RECHAZADOS_COUNT += 1
        motivo = f"Presupuesto excede el límite ({presupuesto} € > 30000 €)"

    # Actualizar la ficha en la Base de Datos
    query_update = "UPDATE solicitudes SET estado = ? WHERE id = ?;"
    cursor.execute(query_update, (nuevo_estado, id_solicitud))
    
    print(f"ID {id_solicitud} | {nombre_empresa}")
    print(f"   ↳ Presupuesto: {presupuesto} €")
    print(f"   ↳ Decisión: {nuevo_estado} ({motivo})\n")

# 5. Guardar los cambios y cerrar
conexion.commit()
conexion.close()

print(f"🎉 Evaluación finalizada: {APROBADOS_COUNT} Aprobadas | {RECHAZADOS_COUNT} Rechazadas.")
