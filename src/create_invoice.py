from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf_utils import extract_currency_value, extract_client_info_from_pdf, get_client_name_and_address_from_string, \
    get_contractor_name_and_address_from_string
import locale
import time
import os


def create_invoice():
    # Get the current Unix timestamp
    unix_timestamp = time.time()

    # Convert the timestamp to a struct_time object
    time_struct = time.localtime(unix_timestamp)

    # Format the date string using strftime
    date_string = time.strftime('%d/%m/%Y', time_struct)

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    # Create a new PDF with Reportlab
    pdf = canvas.Canvas("invoice.pdf", pagesize=letter)

    invoice_number = str(unix_timestamp)[-7:]
    invoice_date = date_string
    invoice_path = os.path.join("attachments", "temp_invoice.pdf")
    client_info = extract_client_info_from_pdf(invoice_path)
    client_name, client_address = get_client_name_and_address_from_string(client_info)
    my_name, my_address = get_contractor_name_and_address_from_string(invoice_path)

    item1 = "Software Development"
    quantity = 1
    price = float(extract_currency_value(invoice_path))
    subtotal = price * quantity
    tax_rate = 0.0
    tax = subtotal * tax_rate
    total = subtotal + tax

    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(50, 750, f"INVOICE #{invoice_number}")
    pdf.setFont("Helvetica", 12)

    pdf.drawString(400, 735, f"Date: {invoice_date}")

    # Client information
    pdf.drawString(50, 700, f"Bill to:")
    pdf.drawString(50, 685, f"{client_name}")
    # Split the address into lines with a maximum of 30 characters each
    address_lines = [client_address[i:i + 30] for i in range(0, len(client_address), 30)]

    # Draw each line of the address separately
    y = 670
    for line in address_lines:
        pdf.drawString(50, y, line)
        y -= 15  # Adjust y-coordinate for next line

    my_name_lines = [my_name[i:i + 30] for i in range(0, len(my_name), 30)]
    my_address_lines = [my_address[i:i + 30] for i in range(0, len(my_address), 30)]

    my_info = my_name_lines + my_address_lines

    pdf.drawString(350, 700, f"Billed by:")

    y = 685
    for line in my_info:
        pdf.drawString(350, y, line)
        y -= 15  # Adjust y-coo

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
