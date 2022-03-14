from src.parsing.html_to_text.html_to_text import html_to_text_converter
from src.settings import HMTL_TO_ORDERED_SENT


def do():
    html_to_text_converter(
        HMTL_TO_ORDERED_SENT['SOURCE_PATH'],
        HMTL_TO_ORDERED_SENT['DESTINATION_PATH'],
    )