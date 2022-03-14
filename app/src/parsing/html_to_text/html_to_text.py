from bs4 import BeautifulSoup
from src.parsing.html_to_text.common import ResumeType
from src.parsing.html_to_text.column_cv import column_traverse
from src.parsing.html_to_text.paragraph_cv import paragraph_traverse


def html_to_text_converter(source_path, destination_path, resume_type: ResumeType = ResumeType.PARAGRAPH):
    """
    :param source_path: path to input html-file
    :param destination_path: path to output text-file
    :param resume_type: PARAGRAPH or COLUMN
    :return: None
    """
    with open(source_path, 'r') as source, open(destination_path, 'w') as destination:
        soup = BeautifulSoup(source, 'lxml', multi_valued_attributes=None)

        if resume_type == ResumeType.PARAGRAPH:
            paragraph_traverse(soup.body, destination)
        else:
            column_traverse(soup.body, destination)
