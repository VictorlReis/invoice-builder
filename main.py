from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf_utils import extract_currency_value
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR')
# Create a new PDF with Reportlab
pdf = canvas.Canvas("invoice.pdf", pagesize=letter)

invoice_number = "5"
invoice_date = "2023-02-16"
client_name = "John Doe"
client_address = "123 Main St, Anytown USA"
# myINFO
my_name = "Victor"
my_address = "456 Oak St, Anytown USA"

item1 = "Software Development"
quantity = 1
price = locale.atof(extract_currency_value("cambio.pdf"))
subtotal = price * quantity
tax_rate = 0.0
tax = subtotal * tax_rate
total = subtotal + tax


pdf.setFont("Helvetica-Bold", 25)
pdf.drawString(50, 750, f"INVOICE #{invoice_number}")
pdf.setFont("Helvetica", 12)

pdf.drawString(400, 735, f"Date: {invoice_date}")

# Client information
pdf.drawString(50, 700, f"Bill by:")
pdf.drawString(50, 685, f"{client_name}")
pdf.drawString(50, 670, f"{client_address}")

pdf.drawString(400, 700, f"Billed to:")
pdf.drawString(400, 685, f"{my_name}")
pdf.drawString(400, 670, f"{my_address}")

# Table header
pdf.setFillColorRGB(0.85, 0.85, 0.85)
pdf.rect(50, 590, 500, 20, fill=True)
pdf.setFillColorRGB(0, 0, 0)
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(60, 596, "Item")
pdf.drawString(300, 596, "Quantity")
pdf.drawString(450, 596, "Amount")

# Table rows
pdf.setFont("Helvetica", 12)
pdf.drawString(60, 570, item1)
pdf.drawString(300, 570, f"{quantity}")
pdf.drawString(450, 570, f"${price:.2f}")

# Total
pdf.setFont("Helvetica", 12)
pdf.drawString(400, 500, f"Subtotal:")
pdf.drawRightString(550, 500, f"${subtotal:.2f}")
pdf.drawString(400, 480, f"Tax:")
pdf.drawRightString(550, 480, f"${tax:.2f}")
pdf.line(400, 470, 550, 470)
pdf.drawString(400, 450, "Total:")
pdf.drawRightString(550, 450, f"${total:.2f}")

# Notes
pdf.setFont("Helvetica", 12)
pdf.drawString(50, 420, "Notes:")
pdf.drawString(50, 400, "Thank you for your business!")
pdf.drawString(50, 380, "Please make payment within 30 days.")

pdf.save()
