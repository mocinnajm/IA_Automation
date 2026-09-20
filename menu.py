import os
import subprocess
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_BIN = os.path.join(BASE_DIR, "env_gemini", "bin", "python3")

# Si no encuentra la ruta relativa, usa el python activo del sistema
if not os.path.exists(PYTHON_BIN):
    PYTHON_BIN = "python3"

def limpiar_pantalla():
    os.system('clear')

def mostrar_menu():
    limpiar_pantalla()
    print("==========================================")
    print("   🤖 PANEL DE CONTROL - IA AUTOMATION    ")
    print("==========================================")
    print("1. 📄 Procesar lote de documentos (Entrada -> IA -> BD)")
    print("2. 🔍 Ejecutar Inspector (Evaluar Reglas de Negocio)")
    print("3. 📊 Ver estado de la Base de Datos (SQLite)")
    print("4. 📝 Ver libro de registros del sistema (sistema.log)")
    print("5. 📖 Leer Apuntes de Teoría")
    print("6. 🚪 Salir")
    print("==========================================")

def ver_base_datos():
    db_path = os.path.join(BASE_DIR, "4_Bases_Datos", "subvenciones.db")
    if not os.path.exists(db_path):
        print("\n❌ La base de datos no existe todavía.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, empresa, presupuesto, cumple_requisitos, estado FROM solicitudes")
        filas = cursor.fetchall()
        print("\n--- 📊 CONTENIDO DE LA BASE DE DATOS ---")
        if not filas:
            print("La tabla está vacía.")
        else:
            print(f"{'ID':<4} | {'Empresa':<25} | {'Presupuesto':<12} | {'Requisitos':<10} | {'Estado':<10}")
            print("-" * 70)
            for f in filas:
                req = "Sí" if f[3] else "No"
                print(f"{f[0]:<4} | {f[1]:<25} | {f[2]:<12.2f} | {req:<10} | {f[4]:<10}")
    except sqlite3.OperationalError:
        print("\n⚠️ La tabla 'solicitudes' aún no ha sido creada.")
    finally:
        conn.close()

def ver_logs():
    log_path = os.path.join(BASE_DIR, "sistema.log")
    if not os.path.exists(log_path):
        print("\n❌ El archivo sistema.log no existe todavía.")
        return
    print("\n--- 📝 ÚLTIMOS REGISTROS DEL SISTEMA ---")
    os.system(f"tail -n 15 '{log_path}'")

def ver_teoria():
    teoria_path = os.path.join(BASE_DIR, "1_Teoria", "Conceptos_Clave.md")
    if not os.path.exists(teoria_path):
        print("\n❌ El archivo de teoría no existe.")
        return
    limpiar_pantalla()
    with open(teoria_path, 'r', encoding='utf-8') as f:
        print(f.read())

def principal():
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción (1-6): ").strip()

        if opcion == "1":
            print("\n🚀 Ejecutando procesador de lote...")
            script = os.path.join(BASE_DIR, "3_Proyectos_Completos", "procesar_lote.py")
            subprocess.run([PYTHON_BIN, script])
            input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            print("\n🔍 Ejecutando inspector de reglas...")
            script = os.path.join(BASE_DIR, "3_Proyectos_Completos", "evaluar_solicitudes.py")
            subprocess.run([PYTHON_BIN, script])
            input("\nPresiona Enter para continuar...")

        elif opcion == "3":
            ver_base_datos()
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":
            ver_logs()
            input("\nPresiona Enter para continuar...")

        elif opcion == "5":
            ver_teoria()
            input("\nPresiona Enter para continuar...")

        elif opcion == "6":
            print("\n👋 ¡Hasta luego, Mohcine!")
            break

        else:
            input("\n⚠️ Opción no válida. Presiona Enter e intenta de nuevo...")

if __name__ == "__main__":
    principal()
