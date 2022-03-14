from src.parsing.pdf_to_html import pdf_to_html_converter
from src.settings import PDF_TO_HTML


def do():
    pdf_to_html_converter((
        PDF_TO_HTML['SOURCE_PATH'],
        PDF_TO_HTML['DESTINATION_PATH']
    ))