import pytest
import sqlite3

# 1. FIXTURE: Prepara una base de datos temporal en memoria (:memory:)
@pytest.fixture
def db_en_memoria():
    # Arrange (Preparación global)
    conexion = sqlite3.connect(":memory:")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT,
            cif TEXT,
            presupuesto REAL,
            cumple_requisitos BOOLEAN,
            estado TEXT
        )
    """)
    conexion.commit()
    
    yield conexion  # Entrega la conexión limpia al test
    
    conexion.close() # Se limpia y destruye automáticamente al terminar

# 2. TEST: Guardar e inspeccionar un registro
def test_insertar_y_consultar_solicitud(db_en_memoria):
    cursor = db_en_memoria.cursor()
    
    # Act (Actuar: Insertar un dato ficticio)
    cursor.execute("""
        INSERT INTO solicitudes (empresa, cif, presupuesto, cumple_requisitos, estado)
        VALUES ('Innovacion SL', 'B12345678', 45000, 1, 'APROBADO')
    """)
    db_en_memoria.commit()
    
    # Assert (Comprobar: ¿Se ha guardado correctamente?)
    cursor.execute("SELECT empresa, estado FROM solicitudes WHERE cif = 'B12345678'")
    resultado = cursor.fetchone()
    
    assert resultado is not None
    assert resultado[0] == "Innovacion SL"
    assert resultado[1] == "APROBADO"
