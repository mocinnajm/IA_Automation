# 🧪 APUNTES DE TEORÍA: TESTING Y CALIDAD CÓDIGO (PYTEST)

---

## 🧠 1. Conceptos Clave para Respuestas en Entrevistas

* **Prueba Unitaria (Unit Test):** Un pequeño bloque de código que comprueba el funcionamiento de una función aislada. Sirve para detectar errores antes de subir cambios a producción.
* **Estructura AAA (Arrange, Act, Assert):**
  1. **Arrange (Preparar):** Crear los datos o condiciones iniciales.
  2. **Act (Ejecutar):** Llamar a la función que queremos probar.
  3. **Assert (Comprobar):** Verificar que el resultado sea el esperado (`assert resultado == esperado`).
* **Mocks (Simulaciones):** Objetos falsos que simulan servicios externos (como la API de Gemini o un envío de emails). Permiten probar el código sin realizar llamadas de red reales, evitando gasto de dinero, lentitud o fallos de conexión.
* **Fixtures:** Funciones especiales de Pytest para preparar entornos limpios antes de cada test (por ejemplo, crear una base de datos SQLite temporal en memoria `:memory:` que se borra al terminar la prueba).
* **Control de Excepciones (`pytest.raises`):** Pruebas enfocadas en verificar que el programa lance un error controlado ante datos inválidos en lugar de colapsar.
* **Cobertura de Código (Coverage):** Porcentaje de líneas de código fuente que ejecutan tus pruebas. En la industria se busca habitualmente entre un **70% y un 85%**.

---

## 💡 2. Frases Listas para Memorizar (Para la Entrevista)

* **¿Cómo pruebas tu código?** 
  > "Escribo pruebas unitarias con Pytest aplicando la estructura AAA para validar tanto los flujos correctos como la captura de errores."
* **¿Cómo testeas llamadas a APIs externas?** 
  > "Uso Mocks para simular las respuestas de la API, aislando la lógica y haciendo las pruebas rápidas y sin coste."
* **¿Cómo pruebas bases de datos sin ensuciar producción?** 
  > "Uso Fixtures para levantar bases de datos SQLite en memoria (`:memory:`), ejecutando cada test en un entorno totalmente aislado."
* **¿Cómo aseguras la calidad de tus tests?** 
  > "Analizo la cobertura de código con `pytest-cov` para identificar líneas no probadas y validar los casos límite (*edge cases*)."

---

## 💻 3. Comandos Esenciales de Terminal

* `pytest -v` -> Ejecuta todas las pruebas mostrando el detalle paso a paso.
* `pytest --cov=.` -> Muestra el porcentaje de cobertura total del proyecto.
* `pytest --cov=. --cov-report=term-missing` -> Muestra el mapa de líneas exactas que faltan por probar.
* `pytest --cov=. --cov-report=html` -> Genera un informe visual interactivo en HTML dentro de `htmlcov/index.html`.
