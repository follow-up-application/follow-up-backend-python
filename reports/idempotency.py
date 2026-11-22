import hashlib
from django.http import JsonResponse
from reports.models import DocumentJob

# Rutas que requieren control estricto de no duplicacion
POST_PATHS = ("/api/v1/reportes/", "/api/v1/certificados/")


class IdempotencyMiddleware:
    """
    Middleware que garantiza que peticiones POST repetidas con la misma Idempotency-Key
    no generen documentos duplicados ni sobrecarguen el servidor.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo auditar peticiones POST a las rutas de generacion de documentos
        if request.method != "POST" or not request.path.startswith(POST_PATHS):
            return self.get_response(request)

        key = request.headers.get("Idempotency-Key", "")
        if len(key) < 8:
            return JsonResponse(
                {"error": {"code": "IDEMPOTENCY_KEY_REQUIRED", "message": "Idempotency-Key obligatoria."}},
                status=400,
            )

        raw = request.body
        request_hash = hashlib.sha256(raw).hexdigest()

        # Verificar si ya existe un trabajo con esta misma clave
        existing = DocumentJob.objects.filter(idempotency_key=key).first()
        if existing:
            # Si reutilizan la clave con un cuerpo diferente, es un conflicto
            if existing.request_hash != request_hash:
                return JsonResponse(
                    {"error": {"code": "IDEMPOTENCY_KEY_REUSED", "message": "La clave de idempotencia ya fue usada para otro pedido."}},
                    status=409,
                )
            # Si es el mismo pedido, devolvemos el mismo job existente sin duplicar proceso
            return JsonResponse(
                {"id": str(existing.id), "estado": existing.estado, "url": f"/api/v1/documentos/{existing.id}"},
                status=202,
            )

        # Inyectar en el request para que la vista guarde la clave
        request.idempotency_key = key
        request.request_hash = request_hash
        return self.get_response(request)
