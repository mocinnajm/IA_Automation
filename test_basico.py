# 1. Nuestra función (la que queremos probar)
def calcular_iva(precio_base):
    return precio_base * 1.21

# 2. Nuestra prueba unitaria (siempre debe empezar por la palabra "test_")
def test_calcular_iva_correcto():
    # Arrange (Preparar los datos)
    precio = 100
    
    # Act (Actuar: llamar a la función)
    resultado = calcular_iva(precio)
    
    # Assert (Comprobar: ¿Es 121?)
    assert resultado == 121.0
