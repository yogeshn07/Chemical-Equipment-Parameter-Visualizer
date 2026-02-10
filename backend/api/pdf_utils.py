from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_pdf_report(dataset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Chemical Equipment Report")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Total Equipment: {dataset.total_equipment}")
    y -= 20

    p.drawString(50, y, f"Average Flowrate: {dataset.avg_flowrate:.2f}")
    y -= 20

    p.drawString(50, y, f"Average Pressure: {dataset.avg_pressure:.2f}")
    y -= 20

    p.drawString(50, y, f"Average Temperature: {dataset.avg_temperature:.2f}")
    y -= 30

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Equipment Type Distribution")
    y -= 25

    p.setFont("Helvetica", 12)
    for eq_type, count in dataset.equipment_type_distribution.items():
        p.drawString(60, y, f"{eq_type}: {count}")
        y -= 18

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
