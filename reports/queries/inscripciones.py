from typing import Any
from reports.queries.base import execute_query


def query_inscripciones(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene el padron general de inscripciones por ciclo lectivo, curso o materia.
    """
    sql = """
    SELECT cd.curso, cd.division, cd.turno,
           m.nombre AS materia,
           u.first_name || ' ' || u.last_name AS alumno,
           i.estado,
           TO_CHAR(i.fecha_inscripcion, 'YYYY-MM-DD') AS fecha_inscripcion
    FROM inscripciones i
    JOIN materias m ON m.id = i.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    JOIN alumnos al ON al.id = i.alumno_id
    JOIN users u ON u.id = al.id
    WHERE cd.ciclo_lectivo_id = %(ciclo_id)s::uuid
      AND (%(curso_id)s::bigint IS NULL OR cd.id = %(curso_id)s::bigint)
      AND (%(estado)s IS NULL OR i.estado = %(estado)s)
    ORDER BY cd.curso, cd.division, alumno, m.nombre;
    """

    params = {
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
        "curso_id": filtros.get("cursoDivisionTurnoId") or filtros.get("curso_id"),
        "estado": filtros.get("estado"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Curso", "Division", "Turno", "Materia", "Alumno", "Estado", "Fecha Inscripcion"]
    titulo = "Padron de Inscripciones"

    return columnas, filas, titulo


def query_inscripcion_certificado(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene las materias inscritas de un alumno para emitir la constancia oficial de inscripcion.
    """
    sql = """
    SELECT m.nombre AS materia,
           cd.curso, cd.division, cd.turno,
           i.estado,
           TO_CHAR(i.fecha_inscripcion, 'YYYY-MM-DD') AS fecha_inscripcion
    FROM inscripciones i
    JOIN materias m ON m.id = i.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    WHERE i.alumno_id = %(alumno_id)s::uuid
      AND cd.ciclo_lectivo_id = %(ciclo_id)s::uuid
      AND (%(estado)s IS NULL OR i.estado = %(estado)s)
    ORDER BY m.nombre;
    """

    params = {
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
        "estado": filtros.get("estado"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Materia", "Curso", "Division", "Turno", "Estado", "Fecha Inscripcion"]
    titulo = "Constancia de Inscripcion"

    return columnas, filas, titulo
