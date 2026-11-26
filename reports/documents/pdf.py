from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def build_pdf(path: Path, *, titulo: str, columnas: list[str], filas: list[list], institucion: str = "Institucion Educativa") -> None:
    """
    Genera un documento PDF tabular estandar con diseno institucional,
    margenes profesionales y filas alternadas.
    """
    font_path = Path(__file__).parent / "templates" / "DejaVuSans.ttf"
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", str(font_path)))
        font_name = "DejaVu"
    else:
        font_name = "Helvetica"

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    estilos = getSampleStyleSheet()
    estilos["Title"].fontName = font_name
    estilos["Normal"].fontName = font_name

    # Armar la matriz de datos: primera fila = encabezados, siguientes = datos
    data = [list(columnas)] + [["" if v is None else str(v) for v in fila] for fila in filas]

    tabla = Table(data, repeatRows=1, hAlign="LEFT")
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
    ]))

    elementos = [
        Paragraph(institucion, estilos["Heading2"]),
        Paragraph(titulo, estilos["Title"]),
        Spacer(1, 6 * mm),
        tabla,
    ]
    doc.build(elementos)
