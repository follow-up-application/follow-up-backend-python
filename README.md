# FollowUp - Servicio de Reportes y Certificados (Python + Django)

Microservicio especializado para la **generacion asincrona de reportes (PDF y Excel) y certificados oficiales con validacion QR**, perteneciente al Trabajo Final Integrador (TFI) de Programacion.

---

## Arquitectura del Sistema
* **Fachada publica (Node.js API):** Puerta de enlace que atiende al frontend movil/web, valida roles y solicita documentos a este servicio mediante un token interno (\X-Service-Token\).
* **Microservicio de Reportes (Este repositorio - Django):** Lee datos academicos desde PostgreSQL (solo lectura) y genera documentos en segundo plano mediante Celery.
* **Base de Datos (PostgreSQL):** Esquema \public\ para datos academicos y esquema propio \
eportes\ para control de tareas y certificados emitidos.

---

## Requisitos Previos
* **Python:** 3.12 o superior (Probado en Python 3.14).
* **PostgreSQL:** Version 16 (Local o Supabase).
* **Redis:** Para la cola de tareas en segundo plano (Celery).

---

## Guia de Instalacion Rapida (Para el equipo)

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

## Estado del Proyecto (Roadmap)
- [x] Configuracion del entorno virtual y dependencias base.
- [x] Inicializacion del proyecto Django y estructura modular.
- [x] Configuracion de la base de datos PostgreSQL local y Router de solo lectura.
- [x] Modelos de datos (\DocumentJob\ y \Certificate\).
- [x] Middleware de seguridad (\X-Service-Token\) e idempotencia.
- [x] Generadores de documentos (PDF con ReportLab y Excel con XlsxWriter).
- [ ] Tareas asincronas con Celery y Redis.
- [ ] Generacion de especificacion OpenAPI (\openapi.json\) y coleccion Postman.
