from pathlib import Path
import xlsxwriter


def build_xlsx(path: Path, *, titulo: str, columnas: list[str], filas: list[list]) -> None:
    """
    Genera una planilla de calculo Excel (.xlsx) formateada, con memoria constante,
    paneles inmovilizados y autofiltros en las columnas.
    """
    book = xlsxwriter.Workbook(
        str(path),
        {"constant_memory": True, "default_date_format": "yyyy-mm-dd"}
    )
    sheet = book.add_worksheet("Reporte")
    header = book.add_format({"bold": True, "bg_color": "#DCE6F1", "border": 1})

    # Escribir titulo principal
    sheet.write(0, 0, titulo, header)

    # Escribir nombres de columnas
    for col, nombre in enumerate(columnas):
        sheet.write(1, col, nombre, header)

    # Escribir las filas de datos
    for row, fila in enumerate(filas, start=2):
        for col, valor in enumerate(fila):
            sheet.write(row, col, valor)

    # Inmovilizar encabezados para que no desaparezcan al scrollear
    sheet.freeze_panes(2, 0)

    # Aplicar autofiltros desplegables en todas las columnas
    if filas:
        sheet.autofilter(1, 0, len(filas) + 1, len(columnas) - 1)

    book.close()
