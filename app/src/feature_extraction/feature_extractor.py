import json
import logging

from collections import defaultdict
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine
from app.src.feature_extraction.utils import SymbolToDict

log = logging.getLogger(__name__)


def parse_line(line):
    """
    For each character in the line extract formatting
    :param line: pdfminer structure of line
    :return: dict of features
    """
    if issubclass(line.__class__, LTTextLine):
        features = defaultdict(list)

        for char in line:
            char_dict = SymbolToDict(char).transform()

            if char_dict is None:
                log.error(f'waited for LTChar or LTAnno '
                          f'instance got instance of a : {char.__class__}\n')
            else:
                for key, value in char_dict.items():
                    features[key].append(value)

        text = line.get_text().replace('\u200b', ' ').replace('\xa0', ' ')

        beginning_of_text = 0
        ending_of_text = len(text) - 1

        for symbol in text:
            if str.isspace(symbol):
                beginning_of_text += 1
            else:
                break

        for symbol in text[::-1]:
            if str.isspace(symbol):
                ending_of_text -= 1
            else:
                break

        for key in features:
            features[key] = features[key][beginning_of_text:ending_of_text + 1]

        features['text'] = text.strip()

        return features
    else:
        log.error(f'waited for LTTextLine subclass got {line.__class__}\n')


def parse_object(text_object, line_id):
    """
    Walk over object and parse each line
    :param text_object: pdfminer structure of object
    :param line_id: current line number
    :return: dict of features, number if current line
    """
    feature_dictionary = dict()
    for line in text_object:
        if issubclass(line.__class__, LTTextLine):
            feature_dictionary[line_id] = parse_line(line)
            line_id += 1
    return feature_dictionary, line_id


def parse_page(page, line_id):
    """
    Walk over page and run 'parse_object' on each obj
    :param page: pdfminer structure of page
    :param line_id: current line number
    :return: dict of features, number if current line
    """
    feature_dictionary = {}
    for text_object in page:
        if issubclass(text_object.__class__, LTTextBox):
            parsed_obj, line_id = parse_object(text_object, line_id)
            feature_dictionary.update(parsed_obj)
    return feature_dictionary, line_id


def feature_extractor(source_path, destination_path):
    """
    Walk over pdf file from source_path and extract features for each row. Save received structure to json file
    :param source_path: path to pdf file
    :param destination_path: path to output dir
    :return: None
    """
    line_id = 0
    feature_dictionary = {}

    with open(destination_path, 'w') as destination:
        for page_layout in extract_pages(source_path):
            parsed_page, line_id = parse_page(page_layout, line_id)
            feature_dictionary.update(
               parsed_page
            )
        json.dump(feature_dictionary, destination)

