import PyPDF2
import re


def extract_text_from_pdf(pdf_file_path):
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page_text = pdf_reader.pages[0].extract_text()
    pdf_file.close()
    print(page_text)
    return page_text


def extract_currency_value(pdf_file_path):
    pdf_text = extract_text_from_pdf(pdf_file_path)
    pattern = r'USD\s+([\d,\.]+)\s*\('
    match = re.search(pattern, pdf_text)

    if match:
        return match.group(1)
    else:
        print("No match found")
