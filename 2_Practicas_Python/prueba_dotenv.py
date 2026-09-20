import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv(dotenv_path=os.path.expanduser("~/IA_Automation/.env"))

# Recuperar la variable
clave_recuperada = os.getenv("GEMINI_API_KEY")

print("--- 🔐 PRUEBA DE SEGURIDAD CON .ENV ---")
if clave_recuperada:
    print(f"✅ Éxito: La clave se ha leído correctamente desde el .env.")
    print(f"🔒 Muestra de la clave (oculta por seguridad): {clave_recuperada[:5]}*****")
else:
    print("❌ Error: No se ha podido leer la variable GEMINI_API_KEY.")
