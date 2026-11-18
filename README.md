# FollowUp - Servicio de Reportes y Certificados (Python + Django)

Microservicio especializado para la **generación asíncrona de reportes (PDF y Excel) y certificados oficiales con validación QR**, perteneciente al Trabajo Final Integrador (TFI) de Programación.

---

## ??? Arquitectura del Sistema
* **Fachada pública (Node.js API):** Puerta de enlace que atiende al frontend móvil/web, valida roles y solicita documentos a este servicio mediante un token interno (\X-Service-Token\).
* **Microservicio de Reportes (Este repositorio - Django):** Lee datos académicos desde PostgreSQL (solo lectura) y genera documentos en segundo plano mediante Celery.
* **Base de Datos (PostgreSQL):** Esquema \public\ para datos académicos y esquema propio \eportes\ para control de tareas y certificados emitidos.

---

## ?? Requisitos Previos
* **Python:** 3.12 o superior (Probado en Python 3.14).
* **PostgreSQL:** Versión 16 (Local o Supabase).
* **Redis:** Para la cola de tareas en segundo plano (Celery).

---

## ?? Guía de Instalación Rápida (Para el equipo)

1. **Clonar el repositorio y entrar en la carpeta:**
   \\\ash
   cd follow-up-backend-python
   \\\

2. **Crear y activar el entorno virtual:**
   * En Windows (PowerShell):
     \\\powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     \\\
   * En Linux / macOS:
     \\\ash
     python3 -m venv .venv
     source .venv/bin/activate
     \\\

3. **Instalar dependencias:**
   \\\ash
   pip install -r requirements.txt
   \\\

4. **Variables de entorno:**
   * Copiar el archivo de ejemplo \.env.example\ a \.env\ y configurar las credenciales locales de PostgreSQL.

---

## ??? Estado del Proyecto (Roadmap)
- [x] Configuración del entorno virtual y dependencias base.
- [ ] Inicialización del proyecto Django y estructura modular.
- [ ] Configuración de la base de datos PostgreSQL local y Router de solo lectura.
- [ ] Modelos de datos (\DocumentJob\ y \Certificate\).
- [ ] Middleware de seguridad (\X-Service-Token\) e idempotencia.
- [ ] Generadores de documentos (PDF con ReportLab y Excel con XlsxWriter).
- [ ] Tareas asíncronas con Celery y Redis.
- [ ] Generación de especificación OpenAPI (\openapi.json\) y colección Postman.
