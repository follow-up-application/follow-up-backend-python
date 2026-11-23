import uuid
from django.db import models


class DocumentJob(models.Model):
    ESTADOS = [
        ("pendiente", "pendiente"),
        ("procesando", "procesando"),
        ("listo", "listo"),
        ("fallido", "fallido"),
        ("cancelado", "cancelado"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=40)
    formato = models.CharField(max_length=4)
    estado = models.CharField(max_length=16, default="pendiente")
    solicitado_por = models.UUIDField()
    request_id = models.CharField(max_length=100, blank=True)
    idempotency_key = models.CharField(max_length=255, unique=True)
    request_hash = models.CharField(max_length=64)
    filtros = models.JSONField(default=dict)
    snapshot = models.JSONField(default=dict, blank=True)
    storage_path = models.CharField(max_length=500, blank=True)
    nombre_archivo = models.CharField(max_length=255, blank=True)
    checksum = models.CharField(max_length=64, blank=True)
    total_filas = models.PositiveIntegerField(default=0)
    progreso = models.PositiveSmallIntegerField(default=0)
    error_code = models.CharField(max_length=50, blank=True)
    error_message = models.TextField(blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["estado", "created_at"]),
            models.Index(fields=["solicitado_por", "created_at"]),
            models.Index(fields=["expires_at"]),
        ]


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=40, unique=True)
    tipo = models.CharField(max_length=40)
    alumno_id = models.UUIDField()
    ciclo_lectivo_id = models.UUIDField()
    job = models.OneToOneField(
        DocumentJob, null=True, blank=True, on_delete=models.SET_NULL, related_name="certificado"
    )
    payload = models.JSONField(default=dict)
    hash_sha256 = models.CharField(max_length=64)
    pdf_path = models.CharField(max_length=500)
    emitido_en = models.DateTimeField(auto_now_add=True)
    anulado = models.BooleanField(default=False)
    anulado_en = models.DateTimeField(null=True, blank=True)
    motivo_anulacion = models.CharField(max_length=500, blank=True)
