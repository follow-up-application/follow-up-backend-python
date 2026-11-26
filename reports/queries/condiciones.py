from typing import Any
from reports.queries.base import execute_query


def verificar_periodo_cerrado(periodo_id: str | None) -> bool:
    """
    Verifica si el periodo academico fue formalmente cerrado en la tabla periodo_cierres.
    """
    if not periodo_id:
        return False
    sql = "SELECT 1 FROM periodo_cierres WHERE periodo_id = %(periodo_id)s::uuid LIMIT 1;"
    _, filas = execute_query(sql, {"periodo_id": periodo_id})
    return len(filas) > 0


def query_condiciones(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene las condiciones finales de los alumnos (regular, libre, promocionado) de un periodo cerrado.
    """
    periodo_id = filtros.get("periodoId") or filtros.get("periodo_id")
    if not verificar_periodo_cerrado(periodo_id):
        raise ValueError("PERIODO_NO_CERRADO")

    sql = """
    SELECT p.nombre AS periodo,
           cd.curso, cd.division, cd.turno,
           m.nombre AS materia,
           u.first_name || ' ' || u.last_name AS alumno,
           ca.condicion,
           ca.promedio,
           ca.porcentaje_asistencia,
           TO_CHAR(ca.calculada_en, 'YYYY-MM-DD HH24:MI') AS calculada_en
    FROM condiciones_alumno ca
    JOIN periodos p ON p.id = ca.periodo_id
    JOIN materias m ON m.id = ca.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    JOIN alumnos al ON al.id = ca.alumno_id
    JOIN users u ON u.id = al.id
    WHERE ca.periodo_id = %(periodo_id)s::uuid
      AND (%(curso_id)s::bigint IS NULL OR cd.id = %(curso_id)s::bigint)
    ORDER BY cd.curso, cd.division, alumno, m.nombre;
    """

    params = {
        "periodo_id": periodo_id,
        "curso_id": filtros.get("cursoDivisionTurnoId") or filtros.get("curso_id"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Periodo", "Curso", "Division", "Turno", "Materia", "Alumno", "Condicion", "Promedio", "% Asistencia", "Fecha Calculo"]
    titulo = "Reporte de Condiciones Finales"

    return columnas, filas, titulo


def query_regularidad(filtros: dict[str, Any], snapshot: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]], str]:
    """
    Obtiene las materias regulares o promocionadas vigentes para la constancia de regularidad.
    """
    sql = """
    SELECT DISTINCT ON (ca.alumno_id, m.id)
           m.nombre AS materia,
           ca.condicion,
           ca.promedio,
           ca.porcentaje_asistencia,
           TO_CHAR(ca.calculada_en, 'YYYY-MM-DD') AS fecha
    FROM condiciones_alumno ca
    JOIN materias m ON m.id = ca.materia_id
    JOIN curso_division_turno cd ON cd.id = m.curso_division_turno_id
    WHERE ca.alumno_id = %(alumno_id)s::uuid
      AND cd.ciclo_lectivo_id = %(ciclo_id)s::uuid
      AND ca.condicion IN ('regular', 'promocionado')
    ORDER BY ca.alumno_id, m.id, ca.calculada_en DESC;
    """

    params = {
        "alumno_id": filtros.get("alumnoId") or filtros.get("alumno_id"),
        "ciclo_id": filtros.get("cicloLectivoId") or filtros.get("ciclo_id"),
    }

    _, filas = execute_query(sql, params)
    columnas = ["Materia", "Condicion", "Promedio", "% Asistencia", "Fecha de Regularidad"]
    titulo = "Constancia de Alumno Regular"

    return columnas, filas, titulo
