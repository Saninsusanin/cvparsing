from src.parsing.html_to_text.html_to_text import html_to_text_converter
from src.parsing.pdf_to_html import pdf_to_html_converter
from src.parsing.utils import transform, pdf_to_html_paths, html_to_text_paths
from src.settings import PDF_TO_TEXT_BATCH


def do():
    transform(
        PDF_TO_TEXT_BATCH['PDF_DIR_PATH'],
        PDF_TO_TEXT_BATCH['HTML_DIR_PATH'],
        pdf_to_html_converter,
        pdf_to_html_paths
    )
    transform(
        PDF_TO_TEXT_BATCH['HTML_DIR_PATH'],
        PDF_TO_TEXT_BATCH['TEXT_DIR_PATH'],
        html_to_text_converter,
        html_to_text_paths
    )