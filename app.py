import streamlit as st
import os

# Configuración de la página web
st.set_page_config(
    page_title="Evaluador de Subvenciones IA",
    page_icon="🤖",
    layout="centered"
)

# Título y descripción principal
st.title("🤖 Evaluador Inteligente de Documentos")
st.write("Sube una solicitud en formato PDF o TXT para analizarla con IA y evaluar su aprobación.")

st.divider()

# 1. Componente para subir archivos
archivo_subido = st.file_uploader(
    "Selecciona un archivo desde tu equipo", 
    type=["txt", "pdf"]
)

# 2. Botón de procesamiento
if archivo_subido is not None:
    st.info(f"📄 Archivo cargado: **{archivo_subido.name}**")
    
    if st.button("🚀 Procesar Documento con IA", use_container_width=True):
        with st.spinner("Analizando contenido con Gemini y aplicando reglas..."):
            # Simulamos el procesamiento conectando con la lógica de negocio
            # (Aquí es donde Streamlit llama a tus scripts de Pydantic/Base de datos)
            
            # Muestra de resultado visual
            st.success("✅ **Resultado de la Evaluación: APROBADO**")
            
            st.subheader("📊 Detalle del Análisis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Presupuesto Solicitado", value="4.500 €")
            with col2:
                st.metric(label="Estado de Reglas", value="Cumple requisitos")

            st.json({
                "solicitante": "Ejemplo Demo",
                "concepto": "Desarrollo de Software",
                "estado": "Aprobado",
                "motivo": "Presupuesto dentro del límite autorizado (< 5.000 €)"
            })

else:
    st.warning("Por favor, sube un archivo para habilitar el análisis.")
