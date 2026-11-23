import secrets
from rest_framework.permissions import BasePermission
from django.conf import settings


class ServiceTokenPermission(BasePermission):
    """
    Permiso que valida que la peticion incluya el header X-Service-Token
    coincidente con el token configurado entre Node.js y Django.
    """
    def has_permission(self, request, view):
        # Permitir que las rutas de health check no requieran token
        if getattr(view, "allow_anonymous", False):
            return True

        token = request.headers.get("X-Service-Token", "")
        return secrets.compare_digest(token, settings.SERVICE_TOKEN)
