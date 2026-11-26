from typing import Any
from django.db import connections


def execute_query(sql: str, params: dict[str, Any] | None = None) -> tuple[list[str], list[list[Any]]]:
    """
    Ejecuta una consulta SQL de solo lectura contra la base academica 'follow'.
    Retorna una tupla (columnas, filas).
    """
    if params is None:
        params = {}

    with connections["follow"].cursor() as cursor:
        cursor.execute(sql, params)
        columnas = [col[0] for col in cursor.description] if cursor.description else []
        filas = [list(row) for row in cursor.fetchall()]

    return columnas, filas
