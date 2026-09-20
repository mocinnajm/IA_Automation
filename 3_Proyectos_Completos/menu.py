import os
import subprocess
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../4_Bases_Datos/subvenciones.db")
PYTHON_BIN = os.path.join(BASE_DIR, "../env_gemini/bin/python3")

def ver_base_datos():
    print("\n--- 📊 ESTADO ACTUAL DE LA BASE DE DATOS ---")
    if not os.path.exists(DB_PATH):
        print("⚠️ La base de datos aún no existe.")
        return
    
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, empresa, presupuesto, estado FROM solicitudes;")
    filas = cursor.fetchall()
    conexion.close()

    if not filas:
        print("ℹ️ No hay registros en la base de datos.")
    else:
        print(f"{'ID':<4} | {'Empresa':<32} | {'Presupuesto':<12} | {'Estado':<10}")
        print("-" * 65)
        for fila in filas:
            print(f"{fila[0]:<4} | {fila[1]:<32} | {fila[2]:<12.2f} | {fila[3]:<10}")
    print()

def ver_teoria():
    print("\n--- 📖 APUNTES RÁPIDOS DE TEORÍA ---")
    teoria_path = os.path.join(BASE_DIR, "../1_Teoria/Conceptos_Clave.md")
    if os.path.exists(teoria_path):
        with open(teoria_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("⚠️ No se encontró el archivo de teoría.")

def mostrar_menu():
    while True:
        print("\n==========================================")
        print("   🤖 PANEL DE CONTROL - IA AUTOMATION   ")
        print("==========================================")
        print("1. 📄 Procesar lote de documentos (Entrada -> IA -> BD)")
        print("2. 🔍 Ejecutar Inspector (Evaluar Reglas de Negocio)")
        print("3. 📊 Ver estado de la Base de Datos")
        print("4. 📖 Leer Apuntes de Teoría")
        print("5. 🚪 Salir")
        
        opcion = input("\nElige una opción (1-5): ").strip()

        if opcion == "1":
            print("\n🚀 Lanzando Procesador de Lotes...")
            script = os.path.join(BASE_DIR, "procesar_lote.py")
            subprocess.run([PYTHON_BIN, script])
        elif opcion == "2":
            print("\n🔍 Lanzando Inspector de Calidad...")
            script = os.path.join(BASE_DIR, "../2_Practicas_Python/evaluar_solicitudes.py")
            subprocess.run([PYTHON_BIN, script])
        elif opcion == "3":
            ver_base_datos()
        elif opcion == "4":
            ver_teoria()
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Elige un número del 1 al 5.")

if __name__ == "__main__":
    mostrar_menu()
