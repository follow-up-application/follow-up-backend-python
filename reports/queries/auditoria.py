from typing import Any
from reports.queries.base import execute_query


def query_auditoria(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene los registros de auditoria del sistema entre fechas con filtros opcionales.
    """
    sql = \"\"\"
    SELECT id,
           entidad,
           entidad_id,
           accion,
           actor_id,
           COALESCE(actor_role, '') AS actor_role,
           COALESCE(motivo, '') AS motivo,
           TO_CHAR(ocurrido_en, 'YYYY-MM-DD HH24:MI:SS') AS ocurrido_en
    FROM auditoria
    WHERE ocurrido_en >= %(desde)s
      AND ocurrido_en < %(hasta)s
      AND (%(actor_id)s::uuid IS NULL OR actor_id = %(actor_id)s::uuid)
      AND (%(accion)s IS NULL OR accion = %(accion)s)
    ORDER BY ocurrido_en DESC
    LIMIT %(limite)s;
    \"\"\"

    params = {
        "desde": filtros.get("desde"),
        "hasta": filtros.get("hasta"),
        "actor_id": filtros.get("actorId") or filtros.get("actor_id"),
        "accion": filtros.get("accion"),
        "limite": filtros.get("limite", 10000),
    }

    _, filas = execute_query(sql, params)
    columnas = ["ID", "Entidad", "ID Entidad", "Accion", "Actor ID", "Rol Actor", "Motivo", "Fecha y Hora"]
    titulo = "Reporte de Auditoria"

    return columnas, filas, titulo
