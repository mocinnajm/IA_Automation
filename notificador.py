import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_notificacion_telegram(mensaje: str) -> bool:
    """Envia un mensaje de texto al chat de Telegram configurado."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: Falta configurar TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en el archivo .env")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        respuesta = requests.post(url, json=payload, timeout=5)
        # Verificamos si la petición HTTP devolvió un código 200 (Éxito)
        return respuesta.status_code == 200
    except Exception as e:
        print(f"❌ Error al conectar con Telegram: {e}")
        return False

if __name__ == "__main__":
    # Prueba directa del modulo
    exito = enviar_notificacion_telegram("🤖 *Inspector IA:* ¡Notificación de prueba configurada correctamente!")
    if exito:
        print("✅ Mensaje enviado a Telegram con éxito.")
    else:
        print("❌ No se pudo enviar el mensaje.")
