import os
import subprocess
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "4_Bases_Datos", "subvenciones.db")

def mostrar_menu():
    while True:
        print("\n==========================================")
        print("   🤖 PANEL DE CONTROL - IA AUTOMATION   ")
        print("==========================================")
        print("1. 📄 Procesar lote de documentos (Entrada -> IA -> BD)")
        print("2. 🔍 Ejecutar Inspector (Evaluar Reglas de Negocio)")
        print("3. 📊 Ver estado de la Base de Datos")
        print("4. 📖 Leer Apuntes de Teoría")
        print("5. 📜 Ver últimos registros (Logs)")
        print("6. 🧹 Reiniciar Base de Datos (Limpiar pruebas)")
        print("7. 🚪 Salir")
        print("==========================================")
        
        opcion = input("\nElige una opción (1-7): ").strip()
        
        if opcion == "1":
            subprocess.run(["python3", os.path.join(BASE_DIR, "3_Proyectos_Completos", "procesar_lote.py")])
        elif opcion == "2":
            subprocess.run(["python3", os.path.join(BASE_DIR, "3_Proyectos_Completos", "evaluar_solicitudes.py")])
        elif opcion == "3":
            mostrar_bd()
        elif opcion == "4":
            print("\nAccediendo a la carpeta de teoría...")
            subprocess.run(["ls", "-la", os.path.join(BASE_DIR, "1_Teoria")])
        elif opcion == "5":
            subprocess.run(["tail", "-n", "20", os.path.join(BASE_DIR, "sistema.log")])
        elif opcion == "6":
            confirmar = input("⚠️ ¿Seguro que quieres borrar todas las solicitudes de la BD? (s/n): ").lower()
            if confirmar == 's':
                reiniciar_bd()
        elif opcion == "7":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")

def mostrar_bd():
    if not os.path.exists(DB_PATH):
        print("\nℹ️ La base de datos aún no existe.")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solicitudes")
    filas = cursor.fetchall()
    conn.close()
    
    if not filas:
        print("\nℹ️ La base de datos está vacía.")
    else:
        print("\n--- CONTENIDO DE LA BASE DE DATOS ---")
        for f in filas:
            print(f"ID: {f[0]} | Empresa: {f[1]} | CIF: {f[2]} | Presupuesto: {f[3]}€ | Requisitos: {f[4]} | Estado: {f[5]}")

def reiniciar_bd():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM solicitudes")
        conn.commit()
        conn.close()
        print("✅ Base de datos limpiada con éxito.")
    else:
        print("ℹ️ No hay base de datos que limpiar.")

if __name__ == "__main__":
    mostrar_menu()
