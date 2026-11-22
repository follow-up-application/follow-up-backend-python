from django.db import connections
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    Formatea las excepciones para mantener el mismo contrato JSON que Node.js:
    { "error": { "code": "...", "message": "...", "details": {...} } }
    """
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    detail = response.data
    if isinstance(detail, dict) and "error" in detail:
        return response
    code = getattr(exc, "code", "validation_error")
    if not isinstance(code, str):
        code = "validation_error"
    response.data = {
        "error": {
            "code": str(code).upper(),
            "message": str(detail),
            "details": detail
        }
    }
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint publico para verificar que el proceso de Django esta vivo.
    """
    return JsonResponse({"status": "ok", "service": "follow-up-reports"})


@api_view(["GET"])
@permission_classes([AllowAny])
def ready_check(request):
    """
    Endpoint de readiness para verificar que las bases de datos estan accesibles.
    """
    db_status = {}
    all_ok = True

    for db_name in ["default", "follow"]:
        try:
            conn = connections[db_name]
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1;")
            db_status[db_name] = "ok"
        except Exception as e:
            db_status[db_name] = f"error: {str(e)}"
            all_ok = False

    status_code = 200 if all_ok else 503
    return JsonResponse(
        {"status": "ready" if all_ok else "unhealthy", "databases": db_status},
        status=status_code
    )
