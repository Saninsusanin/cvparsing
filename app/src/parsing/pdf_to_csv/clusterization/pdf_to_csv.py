import pandas as pd

from pdfminer.layout import LTChar
from typing import Tuple, Dict, List


def letters_to_df(letters: Dict[Tuple[int, int], List[LTChar]]) -> pd.DataFrame:
    """
    This function translates letters dictionary to pandas dataframe with fields:
    * letter_id
    * letter - text that is stored in the current LTChar
    * left - left border of the current LTChar bounding box
    * right - right border of the current LTChar bounding box
    * lower - lower border of the current LTChar bounding box
    * upper - upper border of the current LTChar bounding box
    :param letters: dictionary with tuple composed of the lower and the upper borders of bounding boxes as keys
    and as a values list of all LTChars from .pdf file with these lower and upper borders
    :return: pandas dataframe
    """
    df_dict = dict(letter_id=[], letter=[], left=[], right=[], upper=[], lower=[])
    letter_id = 0

    for key in letters:
        for letter in letters[key]:
            df_dict['letter_id'].append(letter_id)
            df_dict['letter'].append(letter._text)
            df_dict['left'].append(letter.x0)
            df_dict['right'].append(letter.x1)
            df_dict['upper'].append(letter.y1)
            df_dict['lower'].append(letter.y0)

            letter_id += 1

    return pd.DataFrame.from_dict(df_dict)
