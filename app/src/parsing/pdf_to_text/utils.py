import pandas as pd
import matplotlib.pyplot as plt

from typing import Tuple, Union
from pdfminer.layout import LTChar
from matplotlib.patches import Rectangle


def tuple_comparator(key: Tuple[int, int]) -> int:
    """
    This function is used for sorting keys in letters dictionary
    by second value(upper border of a bounding box projection) in a key
    :param key: key of letter dictionary
    :return: second value of a key aka upper border of bounding box
    """

    return key[1]


def distance_between_word_and_next_letter(last_word_last_letter: LTChar, current_letter: LTChar) -> float:
    """
    This function calculates distance between last letter from current last word and current letter
    to understand whether current letter possess to last word or not.
    Last letter of word should be to the left from current letter
    :param last_word_last_letter: the last letter from last processed word
    :param current_letter: the current letter
    :return: distance between current word bounding box and bounding box of the current letter.
    Distance is calculated by x axis(projections of these boxes on x axis)
    """
    return 0 if last_word_last_letter.x1 >= current_letter.x0 else current_letter.x0 - last_word_last_letter.x1


def plot_letters_df(letters_df: pd.DataFrame, title: str, path: str, color_by: Union[type(None), str] = None) -> None:
    fig = plt.gcf()
    ax = plt.gca()

    fig.set_size_inches(10.5 * 2, 18.5 * 2)
    h_min, w_min, w_max, h_max = letters_df.lower.min(), letters_df.left.min(), \
                                 letters_df.right.max(), letters_df.upper.max()
    colors = [plt.cm.tab20(i) for i in range(20)]

    for i, row in letters_df.iterrows():
        r_x = int(row['left'])
        r_y = int(row['lower'])
        r_h = int(row['upper'] - row['lower'])
        r_w = int(row['right'] - row['left'])
        x = r_x + r_w // 2
        y = r_y + r_h // 2

        if color_by is None:
            color = colors[0]
        else:
            color = colors[hash(row[color_by]) % len(colors)]

        rect = Rectangle((r_x, r_y), r_w, r_h, linewidth=1, edgecolor=color, facecolor='none')
        ax.annotate(str(row['letter']), (x, y), color='b', weight='bold',
                    fontsize=8, ha='center', va='center')
        ax.add_patch(rect)

    plt.xlim([w_min - 30, w_max + 30])
    plt.ylim([h_min - 30, h_max + 30])
    plt.title(title)
    plt.savefig(path)
    plt.close(fig)
