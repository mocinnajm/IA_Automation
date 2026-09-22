# 🎨 APUNTES DE TEORÍA: INTERFAZ WEB CON STREAMLIT

---

## 🧠 Conceptos Clave

* **Streamlit:** Librería de Python para crear aplicaciones web interactivas de datos e IA sin necesidad de saber HTML, CSS o JavaScript.
* **Caso de uso:** Crear un panel de control para subir PDFs, procesarlos con Gemini y mostrar si la solicitud está aprobada o rechazada con un diseño limpio.

---

## 💻 Código base (Ejemplo de 15 líneas)

```python
import streamlit as st

st.title("🤖 Evaluador Inteligente de Subvenciones")

archivo = st.file_uploader("Sube tu documento PDF o TXT", type=["pdf", "txt"])

if archivo and st.button("Procesar con IA"):
    st.info("Procesando documento...")
    # Aquí llamamos a la lógica de Gemini y Pydantic
    st.success("✅ Solicitud Aprobada: Cumple con los requisitos.")
