import os
import logging

from pdfminer.high_level import extract_pages
from app.src.parsing.utils import extract_letters
from app.src.parsing.pdf_to_text.utils import plot_letters_df
from parsing.pdf_to_csv.clusterization.pdf_to_csv import letters_to_df
from app.src.parsing.pdf_to_text.algorithms.word_spliter.dots_grid import get_word_ids


log = logging.getLogger(__name__)


def do():
    min_number_of_points_per_segment = 4

    for root, dirs, files in os.walk('./data/pdfs'):
        for file in files:
            if file.endswith('.pdf'):
                title = file.split('.')[0]
                log.info(f'start processing {title} cv')

                for page_number, page in enumerate(extract_pages(os.path.join(root, file))):
                    log.info(f'page number - {page_number}')
                    letters = extract_letters(page)
                    log.info(f'letters were extracted')
                    letters_df = letters_to_df(letters)
                    # this line drops all spaces
                    letters_df.drop(
                        letters_df[[str(letter).isspace() or
                                    letter == '\u200b' or
                                    letter == '\xa0' for letter in letters_df.letter.values.reshape(-1)]].index,
                        inplace=True)
                    log.info(f'letters were converted')
                    letters_df = get_word_ids(letters_df, min_number_of_points_per_segment)
                    log.info(f'words were extracted')
                    path = os.path.join('.', 'data', 'plots', f'{title}_{page_number + 1}.png')
                    plot_letters_df(letters_df, title, path, 'word_id')
                    log.info(f'page - {page_number} from {title} was successfully plotted')
