#!/bin/bash

# 1. Definir la ruta base del proyecto
BASE_DIR="/home/najm/IA_Automation"

# 2. Ir al directorio del proyecto
cd "$BASE_DIR"

# 3. Cargar el entorno virtual de Python
source "$BASE_DIR/env_gemini/bin/activate"

# 4. Cargar las variables de entorno (.env) de forma segura
set -a
source "$BASE_DIR/.env"
set +a

# 5. Ejecutar el procesamiento e inspección
echo "--- Iniciando Cron Job: $(date) ---" >> "$BASE_DIR/sistema.log"
python3 "$BASE_DIR/3_Proyectos_Completos/procesar_lote.py" >> "$BASE_DIR/sistema.log" 2>&1
python3 "$BASE_DIR/3_Proyectos_Completos/evaluar_solicitudes.py" >> "$BASE_DIR/sistema.log" 2>&1
echo "--- Fin de ejecucion Cron Job: $(date) ---" >> "$BASE_DIR/sistema.log"
