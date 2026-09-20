Sistema de automatización de grado de producción diseñado para la extracción, estructuración, persistencia y evaluación automática de solicitudes de subvención utilizando Inteligencia Artificial Generativa.

---

## 🎯 Arquitectura del Sistema

El flujo de trabajo sigue una arquitectura de pipeline por etapas con gestión segura de credenciales, persistencia relacional y trazabilidad completa:

1. **Recepción e Ingesta:** Lectura de documentos de entrada (`.txt`).
2. **Extracción Estructurada con IA:** Procesamiento mediante **Gemini 3.6 Flash** utilizando la librería oficial `google-genai` y esquemas de validación con **Pydantic**.
3. **Persistencia y Estado:** Almacenamiento en base de datos relacional **SQLite** (`subvenciones.db`) registrando la solicitud en estado inicial `PENDIENTE`.
4. **Motor de Reglas de Negocio:** Evaluación automatizada de condiciones financieras y requisitos organizativos para actualizar el estado a `APROBADA` o `RECHAZADA`.
5. **Auditoría y Trazabilidad:** Registro continuo de eventos y manejo de excepciones con reintentos automáticos en `sistema.log`.
6. **Interfaz de Control:** Panel interactivo en consola (`menu.py`) para administrar la ejecución y supervisar el sistema.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.12
- **IA Generativa:** `google-genai` (Modelo: `gemini-3.6-flash`)
- **Validación de Datos:** Pydantic
- **Base de Datos:** SQLite3
- **Seguridad:** `python-dotenv` (Gestión segura de variables de entorno)
- **Log y Auditoría:** Módulo nativo `logging` de Python

---

## 📂 Estructura del Repositorio

```text
IA_Automation/
├── .env                       # Variables de entorno (API Key - Protegido)
├── .env.example               # Plantilla de configuración de entorno
├── requirements.txt           # Dependencias del proyecto
├── sistema.log                # Registro de auditoría y errores
├── menu.py                    # Panel de control interactivo
├── 1_Teoria/                  # Documentación teórica del proyecto
├── 3_Proyectos_Completos/
│   ├── procesar_lote.py       # Ingesta, extracción con IA y carga en DB
│   ├── evaluar_solicitudes.py # Motor de reglas de negocio
│   ├── documentos_nuevos/     # Búfer de documentos entrantes
│   └── documentos_procesados/ # Archivo histórico de documentos
└── 4_Bases_Datos/
    └── subvenciones.db        # Base de datos SQLite
