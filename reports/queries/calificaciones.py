from typing import Any
from reports.queries.base import execute_query


def query_calificaciones(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene el listado de calificaciones detalladas por instancia de evaluacion.
    """
    sql = \"\"\"
    SELECT u.first_name || ' ' || u.last_name AS alumno,
           cd.curso, cd.division, cd.turno,
           m.nombre AS materia,
           p.nombre AS periodo,
           ie.nombre AS instancia,
           ie.tipo,
           ie.peso,
           cal.valor AS calificacion,
           cal.estado
    FROM calificaciones cal
    JOIN instancias_evaluacion ie ON ie.id = cal.instancia_id
    JOIN periodos p ON p.id = ie.periodo_id
    JOIN materias m ON m.id = ie.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    JOIN alumnos al ON al.id = cal.alumno_id
    JOIN users u ON u.id = al.id
    WHERE cal.estado = 'activa'
      AND p.ciclo_lectivo_id = %(ciclo_id)s::uuid
      AND (%(periodo_id)s::uuid IS NULL OR p.id = %(periodo_id)s::uuid)
      AND (%(curso_id)s::bigint IS NULL OR cd.id = %(curso_id)s::bigint)
      AND (%(materia_id)s::bigint IS NULL OR m.id = %(materia_id)s::bigint)
      AND (%(alumno_id)s::uuid IS NULL OR al.id = %(alumno_id)s::uuid)
    ORDER BY alumno, materia, ie.fecha;
    \"\"\"

    params = {
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
        "periodo_id": filtros.get("periodoId") or filtros.get("periodo_id"),
        "curso_id": filtros.get("cursoDivisionTurnoId") or filtros.get("curso_id"),
        "materia_id": filtros.get("materiaId") or filtros.get("materia_id"),
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Alumno", "Curso", "Division", "Turno", "Materia", "Periodo", "Instancia", "Tipo", "Peso", "Calificacion", "Estado"]
    titulo = "Reporte de Calificaciones"

    return columnas, filas, titulo


def query_notas(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene las calificaciones y materias de un alumno para la emision de constancia/certificado de notas.
    """
    sql = \"\"\"
    SELECT m.nombre AS materia,
           p.nombre AS periodo,
           ie.nombre AS instancia,
           ie.tipo,
           cal.valor AS nota
    FROM calificaciones cal
    JOIN instancias_evaluacion ie ON ie.id = cal.instancia_id
    JOIN periodos p ON p.id = ie.periodo_id
    JOIN materias m ON m.id = ie.materia_id
    WHERE cal.estado = 'activa'
      AND cal.alumno_id = %(alumno_id)s::uuid
      AND (%(ciclo_id)s::uuid IS NULL OR p.ciclo_lectivo_id = %(ciclo_id)s::uuid)
      AND (%(periodo_id)s::uuid IS NULL OR p.id = %(periodo_id)s::uuid)
    ORDER BY m.nombre, p.nombre, ie.fecha;
    \"\"\"

    params = {
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
        "periodo_id": filtros.get("periodoId") or filtros.get("periodo_id"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Materia", "Periodo", "Instancia Evaluacion", "Tipo", "Calificacion"]
    titulo = "Constancia de Calificaciones"

    return columnas, filas, titulo
