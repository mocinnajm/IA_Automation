# ⚙️ APUNTES DE TEORÍA: CI/CD Y GITHUB ACTIONS

---

## 🧠 1. Conceptos Clave para Respuestas en Entrevistas

* **CI/CD:** Automatización del ciclo de vida del software (Integración Continua / Despliegue Continuo).
* **Pipeline:** Secuencia de pasos automatizados (descarga de código, instalación, pruebas, despliegue) que se ejecutan al realizar cambios en el repositorio.
* **GitHub Actions:** Servicio integrado de GitHub para crear workflows de CI/CD mediante archivos YAML alojados en `.github/workflows/`.

---

## 💡 2. Frases Listas para Memorizar (Para la Entrevista)

* **¿Cómo garantizas que no se suba código roto a GitHub?**
  > "Tengo configurado un Pipeline de CI en GitHub Actions que ejecuta automáticamente Pytest en cada Pull Request. Si las pruebas no pasan, no se permite fusionar el código."
