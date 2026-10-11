"""Crea los archivos de ejemplo que usan las pruebas (todo sintético, sin datos reales).

Uso: python tests/generar_fixtures.py
Requiere: pillow, reportlab, pypdf
"""
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

FX = Path(__file__).resolve().parent / "fixtures"


def foto(nombre, color, texto):
    im = Image.new("RGB", (1200, 1600), color)
    d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 1140, 1540], outline=(0, 0, 0), width=4)
    d.text((100, 100), texto, fill=(0, 0, 0))
    for i in range(20):
        d.line([100, 200 + i * 60, 1100, 200 + i * 60], fill=(180, 180, 180), width=2)
    im.save(FX / nombre, quality=90)


def main():
    FX.mkdir(exist_ok=True)
    foto("nomina_julio.jpg", (250, 250, 245), "NOMINA JULIO 2026 (EJEMPLO)")
    foto("nomina_junio_foto.jpg", (245, 250, 250), "NOMINA JUNIO 2026 (EJEMPLO)")

    # PDF mínimo de una página
    (FX / "nomina_junio.pdf").write_bytes(
        b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
        b"4 0 obj<</Length 44>>stream\nBT /F1 24 Tf 72 760 Td (NOMINA JUNIO) Tj ET\nendstream endobj\n"
        b"5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n")

    # PDF de 2 páginas
    c = canvas.Canvas(str(FX / "abril_2paginas.pdf"), pagesize=A4)
    for pagina in (1, 2):
        c.setFont("Helvetica-Bold", 20)
        c.drawString(60, 780, f"NOMINA ABRIL 2026 (EJEMPLO) - Pagina {pagina}")
        c.setFont("Helvetica", 11)
        y = 740
        for i in range(30):
            c.drawString(60, y, f"Concepto {i + 1:02d} ........................................ {1000 + i * 12.5:,.2f} EUR")
            y -= 20
        c.rect(50, 60, 495, 720)
        c.showPage()
    c.save()

    # El mismo PDF protegido con contraseña (como hacen muchas empresas con el DNI)
    w = PdfWriter()
    w.append(PdfReader(str(FX / "abril_2paginas.pdf")))
    w.encrypt(user_password="12345678Z", owner_password="owner-pass")
    with open(FX / "abril_protegida.pdf", "wb") as f:
        w.write(f)

    # PDF dañado: empieza como PDF pero no lo es
    (FX / "dañada.pdf").write_bytes(b"%PDF-1.4\n" + b"\x00\x13basura que no es un pdf valido\n" * 50)

    print("Archivos de ejemplo creados en", FX)


if __name__ == "__main__":
    main()
