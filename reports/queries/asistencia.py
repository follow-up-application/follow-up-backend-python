from typing import Any
from reports.queries.base import execute_query


def query_asistencia(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene el listado detallado de asistencias con filtros opcionales.
    """
    sql = """
    SELECT c.fecha,
           cd.curso, cd.division, cd.turno,
           m.nombre AS materia,
           u.first_name || ' ' || u.last_name AS alumno,
           a.estado, COALESCE(a.justificacion, '') AS justificacion
    FROM asistencias a
    JOIN clases c ON c.id = a.clase_id
    JOIN materias m ON m.id = c.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    JOIN alumnos al ON al.id = a.alumno_id
    JOIN users u ON u.id = al.id
    WHERE c.fecha BETWEEN %(desde)s AND %(hasta)s
      AND (%(ciclo_id)s::uuid IS NULL OR cd.ciclo_lectivo_id = %(ciclo_id)s::uuid)
      AND (%(curso_id)s::bigint IS NULL OR cd.id = %(curso_id)s::bigint)
      AND (%(materia_id)s::bigint IS NULL OR m.id = %(materia_id)s::bigint)
      AND (%(alumno_id)s::uuid IS NULL OR a.alumno_id = %(alumno_id)s::uuid)
    ORDER BY c.fecha, cd.curso, cd.division, alumno
    LIMIT %(limite)s;
    """

    params = {
        "desde": filtros.get("desde"),
        "hasta": filtros.get("hasta"),
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
        "curso_id": filtros.get("cursoDivisionTurnoId") or filtros.get("curso_id"),
        "materia_id": filtros.get("materiaId") or filtros.get("materia_id"),
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
        "limite": filtros.get("limite", 10000),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Fecha", "Curso", "Division", "Turno", "Materia", "Alumno", "Estado", "Justificacion"]
    titulo = "Reporte de Asistencia"

    return columnas, filas, titulo


def query_asistencia_certificado(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene el resumen porcentual de asistencia para la emision de una constancia de alumno.
    """
    sql = """
    SELECT al.id AS alumno_id,
           u.first_name || ' ' || u.last_name AS alumno,
           count(*) AS total_clases,
           count(*) FILTER (WHERE a.estado = 'presente') AS presentes,
           count(*) FILTER (WHERE a.estado = 'justificada') AS justificadas,
           count(*) FILTER (WHERE a.estado = 'ausente') AS ausentes,
           round(100.0 * count(*) FILTER (WHERE a.estado IN ('presente', 'justificada'))
                 / NULLIF(count(*), 0), 2) AS porcentaje
    FROM asistencias a
    JOIN clases c ON c.id = a.clase_id
    JOIN materias m ON m.id = c.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    JOIN alumnos al ON al.id = a.alumno_id
    JOIN users u ON u.id = al.id
    WHERE c.fecha BETWEEN %(desde)s AND %(hasta)s
      AND a.alumno_id = %(alumno_id)s::uuid
      AND (%(curso_id)s::bigint IS NULL OR cd.id = %(curso_id)s::bigint)
    GROUP BY al.id, u.first_name, u.last_name;
    """

    params = {
        "desde": filtros.get("desde"),
        "hasta": filtros.get("hasta"),
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
        "curso_id": filtros.get("cursoDivisionTurnoId") or filtros.get("curso_id"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Alumno ID", "Alumno", "Total Clases", "Presentes", "Justificadas", "Ausentes", "% Asistencia"]
    titulo = "Constancia de Asistencia"

    return columnas, filas, titulo
