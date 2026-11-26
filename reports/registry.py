from rest_framework import serializers

from reports.queries.asistencia import query_asistencia, query_asistencia_certificado
from reports.queries.auditoria import query_auditoria
from reports.queries.calificaciones import query_calificaciones, query_notas
from reports.queries.condiciones import query_condiciones, query_regularidad
from reports.queries.inscripciones import query_inscripciones, query_inscripcion_certificado

FORMATOS_REPORTE = {"pdf", "xlsx"}
FORMATOS_CERTIFICADO = {"pdf"}


class BaseDocumentSerializer(serializers.Serializer):
    formato = serializers.ChoiceField(choices=["pdf", "xlsx"])
    solicitadoPor = serializers.UUIDField()
    requestId = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")

    def validate(self, attrs):
        kind = self.context.get("kind", "")
        if kind == "certificado" and attrs.get("formato") != "pdf":
            raise serializers.ValidationError(
                {"formato": "Los certificados solo se generan en PDF."}, code="formato_no_permitido"
            )
        return attrs


class AsistenciaSerializer(BaseDocumentSerializer):
    cicloLectivoId = serializers.UUIDField()
    cursoDivisionTurnoId = serializers.IntegerField(required=False, min_value=1)
    materiaId = serializers.IntegerField(required=False, min_value=1)
    alumnoId = serializers.UUIDField(required=False)
    desde = serializers.DateField()
    hasta = serializers.DateField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["desde"] > attrs["hasta"]:
            raise serializers.ValidationError({"desde": "Debe ser <= hasta."})
        return attrs


class CalificacionesSerializer(BaseDocumentSerializer):
    cicloLectivoId = serializers.UUIDField()
    periodoId = serializers.UUIDField(required=False)
    cursoDivisionTurnoId = serializers.IntegerField(required=False, min_value=1)
    materiaId = serializers.IntegerField(required=False, min_value=1)
    alumnoId = serializers.UUIDField(required=False)


class CondicionesSerializer(BaseDocumentSerializer):
    periodoId = serializers.UUIDField()
    cursoDivisionTurnoId = serializers.IntegerField(required=False, min_value=1)


class InscripcionesSerializer(BaseDocumentSerializer):
    cicloLectivoId = serializers.UUIDField()
    cursoDivisionTurnoId = serializers.IntegerField(required=False, min_value=1)
    estado = serializers.CharField(required=False, allow_blank=True)


class AuditoriaSerializer(BaseDocumentSerializer):
    desde = serializers.DateTimeField()
    hasta = serializers.DateTimeField()
    actorId = serializers.UUIDField(required=False)
    accion = serializers.CharField(required=False, allow_blank=True)
    limite = serializers.IntegerField(required=False, default=10000, max_value=50000)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["desde"] > attrs["hasta"]:
            raise serializers.ValidationError({"desde": "Debe ser <= hasta."})
        return attrs


class RegularidadSerializer(BaseDocumentSerializer):
    alumnoId = serializers.UUIDField()
    cicloLectivoId = serializers.UUIDField()


class CertificadoNotasSerializer(BaseDocumentSerializer):
    alumnoId = serializers.UUIDField()
    cicloLectivoId = serializers.UUIDField()
    periodoId = serializers.UUIDField(required=False)


class CertificadoAsistenciaSerializer(BaseDocumentSerializer):
    alumnoId = serializers.UUIDField()
    cicloLectivoId = serializers.UUIDField()
    desde = serializers.DateField()
    hasta = serializers.DateField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["desde"] > attrs["hasta"]:
            raise serializers.ValidationError({"desde": "Debe ser <= hasta."})
        return attrs


class InscripcionSerializer(BaseDocumentSerializer):
    alumnoId = serializers.UUIDField()
    cicloLectivoId = serializers.UUIDField()
    estado = serializers.CharField(required=False, allow_blank=True)


REPORTES = {
    "asistencia": {"serializer": AsistenciaSerializer, "query": query_asistencia, "titulo": "Reporte de Asistencia"},
    "calificaciones": {"serializer": CalificacionesSerializer, "query": query_calificaciones, "titulo": "Reporte de Calificaciones"},
    "condiciones": {"serializer": CondicionesSerializer, "query": query_condiciones, "titulo": "Reporte de Condiciones Finales"},
    "inscripciones": {"serializer": InscripcionesSerializer, "query": query_inscripciones, "titulo": "Padron de Inscripciones"},
    "auditoria": {"serializer": AuditoriaSerializer, "query": query_auditoria, "titulo": "Reporte de Auditoria"},
}

CERTIFICADOS = {
    "regularidad": {"serializer": RegularidadSerializer, "query": query_regularidad, "titulo": "Constancia de Regularidad"},
    "calificaciones": {"serializer": CertificadoNotasSerializer, "query": query_notas, "titulo": "Constancia de Calificaciones"},
    "asistencia": {"serializer": CertificadoAsistenciaSerializer, "query": query_asistencia_certificado, "titulo": "Constancia de Asistencia"},
    "inscripcion": {"serializer": InscripcionSerializer, "query": query_inscripcion_certificado, "titulo": "Constancia de Inscripcion"},
}
