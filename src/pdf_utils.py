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
    pattern = r'USD\s+([\d,\.]+)\s*Ordenante'
    match = re.search(pattern, pdf_text)

    if match:
        return match.group(1)
    else:
        print("No match found")


def extract_client_info_from_pdf(pdf_file_path):
    pdf_text = extract_text_from_pdf(pdf_file_path)
    pattern = r'Ordenante\s*:\s*([^\n]+)\n([\s\S]+?)\nDetalhes'
    match = re.search(pattern, pdf_text)

    if match:
        return match.group(2)
    else:
        print("No match found")


def get_client_name_and_address_from_string(client_info_string):
    # Remove all new lines and leading/trailing spaces
    address_string = client_info_string.replace('\n', '').strip()

    # Replace any consecutive space characters with a single space character
    address_string = ' '.join(address_string.split())

    # Split the string into two parts - first line and remaining lines
    parts = address_string.split(maxsplit=1)

    if len(parts) == 2:
        # Return a tuple of two strings - the first line and the remaining lines
        return parts[0].strip(), parts[1].strip()
    else:
        # If the input string does not contain any space character, return the original string as the first line
        return address_string, ''


def get_contractor_name_and_address_from_string(pdf_file_path):
    pdf_text = extract_text_from_pdf(pdf_file_path)
    address_matches = re.search(r"(?<=\.com)([\s\S]+?)(?=REF)", pdf_text)
    name_matches = re.search(r"(?<=e-mail:\s)([\s\S]+?)(?= LTDA)", pdf_text)
    address = re.sub(r'\s+', ' ', address_matches.group(1).strip().replace("\n", " "))
    name = name_matches.group(1).strip().replace("\n", " ") + " LTDA"
    return name, address
