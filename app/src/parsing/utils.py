from collections import defaultdict
from typing import Tuple, Dict, List
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTPage


def letter_comparator(letter: LTChar) -> int:
    """
    This function is used for sorting LTChar by left border of a bounding box
    :param letter
    :return: left border of a bounding box
    """
    return letter.x0


def sort_letters(letters: Dict[Tuple[int, int], List[LTChar]]) -> None:
    """
    This function sorts values from letters dictionary by left border of a bounding box
    :param letters: dictionary with tuple composed of the lower and the upper borders of bounding boxes as keys
    and as a values list of all LTChars from .pdf file with these lower and upper borders
    :return: None
    """

    for key in letters:
        letters[key].sort(key=letter_comparator)


def extract_letters(page: LTPage) -> Dict[Tuple[int, int], List[LTChar]]:
    """
    This function extracts each LTChar from each LTPage and saves them to special the dictionary
    :param page: LTPage
    :return: dictionary with tuple composed of the lower and the upper borders of bounding boxes as keys
    and as a values list of all LTChars from .pdf file with these lower and upper borders
    """
    letters = defaultdict(list)

    for text_object in page:
        if issubclass(text_object.__class__, LTTextBox):
            for line in text_object:
                if issubclass(line.__class__, LTTextLine):
                    for character in line:
                        if isinstance(character, LTChar):
                            letters[(character.y0, character.y1)].append(character)

    sort_letters(letters)

    return letters
