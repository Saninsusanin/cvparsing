import logging

from pdfminer.layout import LTChar
from collections import defaultdict
from typing import Tuple, Dict, List
from pdfminer.high_level import extract_pages
from app.src.parsing.utils import extract_letters
from utils import distance_between_word_and_next_letter, tuple_comparator

log = logging.getLogger(__name__)


def process_page_letters(letters: Dict[Tuple[int, int], List[LTChar]], threshold: float = 1e-0) -> str:
    """
    This function returns text in order descending order by upper border of bounding boxes
    and in each exact mach of y axis projections(aka row) of bounding boxes sorts letters in ascending order
    by left border of the current letter bounding box.
    If there is no or little space by x axis between letters in the each row than this unioun of LTChars is called word
    and saves in text without spaces. After each word space is added. And After each row line feed character is added
    :param letters: dictionary with tuple composed of the lower and the upper borders of bounding boxes as keys
    and as a values list of all LTChars from .pdf file with these lower and upper borders
    :param threshold: this parameter defines distance between letters that is not distance between words
    :return: page text
    """
    page_text = []
    words = defaultdict(list)

    for key in sorted(list(letters.keys()), key=tuple_comparator, reverse=True):
        first_letter = letters[key][0]
        page_text.append(first_letter._text)
        words[key].append([first_letter])

        for letter in letters[key][1:]:
            distance = distance_between_word_and_next_letter(words[key][-1][-1], letter)

            if distance < threshold:
                page_text.append(letter._text)
                words[key][-1].append(letter)
            else:
                page_text.append(f' {letter._text}')
                words[key].append([letter])

        page_text.append('\n')

    return ''.join(page_text)


def pdf_to_text(source_path: str, destination_path: str) -> None:
    """
    This function extracts text from .pdf file
    :param source_path: path to .pdf file
    :param destination_path: path to .text file in which the whole processed text will be stored
    :return:
    """
    with open(destination_path, 'w') as destination:
        for page in extract_pages(source_path):
            letters = extract_letters(page)
            page_text = process_page_letters(letters)
            destination.write(page_text.replace('\u200b', '').replace('\xa0', ' '))
