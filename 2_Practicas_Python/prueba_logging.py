import logging
import os

# Configuración del diario de registros
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "sistema.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

print("--- 📝 PROBANDO EL SISTEMA DE LOGGING ---")

# Registramos eventos de prueba
logging.info("El sistema de automatización se ha iniciado correctamente.")
logging.warning("Advertencia: El directorio de descargas está casi lleno.")

# Simulamos un fallo con try / except
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    # logging.error guarda el mensaje en el archivo .log sin romper la ejecución
    logging.error(f"Error detectado durante el cálculo: {e}")

print("✅ Pruebas finalizadas. Revisa el archivo 'sistema.log'.")
