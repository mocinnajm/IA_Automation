import pytest
from unittest.mock import MagicMock

# 1. Función a probar: Evalúa si una solicitud de subvención es APROBADA
def evaluar_regla_subvencion(presupuesto, cumple_requisitos):
    if presupuesto <= 50000 and cumple_requisitos:
        return "APROBADO"
    return "RECHAZADO"

# 2. Test 1: Caso de éxito
def test_evaluar_subvencion_aprobado():
    # Arrange (Preparar)
    presupuesto = 30000
    requisitos = True
    
    # Act (Actuar)
    resultado = evaluar_regla_subvencion(presupuesto, requisitos)
    
    # Assert (Comprobar)
    assert resultado == "APROBADO"

# 3. Test 2: Caso de rechazo por presupuesto alto
def test_evaluar_subvencion_rechazado_presupuesto():
    # Arrange
    presupuesto = 80000
    requisitos = True
    
    # Act
    resultado = evaluar_regla_subvencion(presupuesto, requisitos)
    
    # Assert
    assert resultado == "RECHAZADO"

# 4. Test 3: Uso de Mocks para simular una respuesta de la API de Gemini
def test_procesamiento_con_mock_gemini():
    # Arrange: Creamos un objeto falso (Mock) que simula la respuesta de la API
    respuesta_falsa_gemini = MagicMock()
    respuesta_falsa_gemini.text = '{"empresa": "TechCorp", "presupuesto": 25000}'
    
    # Act: Extraemos el texto simulado
    texto_extraido = respuesta_falsa_gemini.text
    
    # Assert: Comprobamos que el Mock entregó los datos requeridos
    assert "TechCorp" in texto_extraido
# 5. Función que valida el presupuesto (lanza excepción si es <= 0)
def validar_presupuesto_solicitud(presupuesto):
    if presupuesto <= 0:
        raise ValueError("El presupuesto debe ser un número mayor a cero.")
    return True

# 6. Test: Comprobar que SE LANZA la excepción cuando el dato es inválido
def test_validar_presupuesto_error_negativo():
    # Arrange
    presupuesto_invalido = -5000
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        validar_presupuesto_solicitud(presupuesto_invalido)
    
    # Verificamos el mensaje de error
    assert "mayor a cero" in str(exc_info.value)
