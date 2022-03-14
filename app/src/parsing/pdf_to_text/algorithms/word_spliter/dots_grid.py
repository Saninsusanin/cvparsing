import numpy as np
import pandas as pd

from math import fabs
from functools import partial
from collections import Counter
from dataclasses import dataclass
from sklearn.cluster import DBSCAN
from typing import List, Callable, Tuple


@dataclass
class Segment:
    min: int
    max: int


@dataclass
class Letter:
    letter: str
    lower: int
    upper: int
    left: int
    right: int


def _handler(values, func):
    return func(*values)


def df_to_letter_list(letters_df: pd.DataFrame) -> List[Letter]:
    """
    This function converts letters dataframe to list of letters
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :return:
    """
    return [Letter(row['letter'], row['lower'], row['upper'], row['left'], row['right'])
            for _, row in letters_df.iterrows()]


def segment_intersection(first_segment: Segment, second_segment: Segment) -> bool:
    """
    Tihs function checks whether these two segments intersects or not
    :param first_segment: segment that stores minimal border and maximal border
    :param second_segment: segment that stores minimal border and maximal border
    :return: if these two segments intersects return True if not - False
    """
    return second_segment.min <= first_segment.min <= second_segment.max or \
           second_segment.min <= first_segment.max <= second_segment.min


def get_ordinate_distance(first_letter: Letter, second_letter: Letter) -> float:
    """
    This function calculates distance between bounding boxes by y axis.
    Note that first letter upper has to be bigger than second letter upper
    :param first_letter: letter from letters_df
    :param second_letter: letter from letters_df
    :return: distance between projections of letters bounding boxes on the y axis
    """
    if segment_intersection(Segment(first_letter.lower, first_letter.upper),
                            Segment(second_letter.lower, second_letter.upper)):
        return 0
    else:
        return fabs(first_letter.lower - second_letter.upper)


def get_abscissa_distance(first_letter: Letter, second_letter: Letter) -> float:
    """
    This function calculates distance between letters by x axis.
    If their projections on y axis have zero intersection than distance between them is set to zero.
    If these two letters have non-zero intersection by y axis, than distance between x axis projections is calculated.
    Note that first letter left has to be smaller than second_letter left
    :param first_letter: letter from letters_df
    :param second_letter: letter from letters_df
    :return:
    """
    dist = 0

    if segment_intersection(Segment(first_letter.lower, first_letter.upper),
                            Segment(second_letter.lower, second_letter.upper)) \
            and not segment_intersection(Segment(first_letter.left, first_letter.right),
                                         Segment(second_letter.left, second_letter.right)):
        dist = fabs(first_letter.right - first_letter.left)

    return dist


def get_all_possible_distances(letters_df: pd.DataFrame, distance_function: Callable):
    """
    This function calculates distances between all possible pairs of letters from letters_df
    and as a distance function uses distance_function
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :param distance_function:
    :return: numpy array with all binomial(len(letters_df), 2) distance values
    """
    letters_list = df_to_letter_list(letters_df)

    return np.array(list((map(partial(_handler, func=distance_function),
                              [(letters_list[i], letters_list[j]) for i in range(len(letters_list))
                               for j in range(i + 1, len(letters_list))]))))


def get_min_ordinate_distance(letters_df: pd.DataFrame) -> float:
    """
    This function finds minimal non-zero distance between letters by y axis.
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :return: minimum non-zero distance by y axis
    """
    letters_df.sort_values(['upper', 'lower'], ascending=False, inplace=True)
    ordinate_distances = get_all_possible_distances(letters_df, get_ordinate_distance)

    return np.min(ordinate_distances[ordinate_distances > 0])


def get_min_abscissa_distance(letters_df: pd.DataFrame) -> float:
    """
    This function finds minimal non-zero distance between letters by x axis.
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :return: minima non-zero distance by x axis
    """
    letters_df.sort_values(['left'], ascending=True, inplace=True)
    abscissa_distances = get_all_possible_distances(letters_df, get_abscissa_distance)

    return np.min(abscissa_distances[abscissa_distances > 0])


def get_grid_step(letters_df: pd.DataFrame, min_number_of_points_per_segment: int) -> float:
    """
    This function finds grid step if we want to have not less than min_number_of_points_per_segment points per segment.
    In other words in each square with side equal length of a segment
    there will be not less than min_number_of_points_per_segment^2 points
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :param min_number_of_points_per_segment:
    :return: step of such a grid
    """
    min_ordinate_distance = get_min_ordinate_distance(letters_df)
    min_abscissa_distance = get_min_abscissa_distance(letters_df)
    min_letter_height = np.min(letters_df.upper.values.reshape(-1, 1) - letters_df.lower.values.reshape(-1, 1))
    min_letter_width = np.min(np.min(letters_df.right.values.reshape(-1, 1) - letters_df.left.values.reshape(-1, 1)))

    grid_step = min(min_ordinate_distance, min_abscissa_distance,
                    min_letter_height, min_letter_width) / min_number_of_points_per_segment

    return grid_step


def point_generator(segment: Segment, grid_step: float, eps: float = 1e-10):
    """
    This function generates points in segment with step equal grid_step
    :param segment: segment in which we want to generate points
    :param grid_step: step of grid
    :param eps: threshold of float number comparing
    :return: next point in segment
    """
    current_x = (segment.min // grid_step) * grid_step

    if fabs(current_x - segment.min) <= eps:
        yield current_x
    else:
        current_x += grid_step

    while segment.max - current_x >= eps:
        yield current_x
        current_x += grid_step


def get_grid_df(letters_df: pd.DataFrame, min_number_of_points_per_segment: int) -> Tuple[pd.DataFrame, float]:
    """
    This function converts letters_df to new dataframe with points
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :param min_number_of_points_per_segment:
    :return: dataframe with three fields: letter_id and its coordinates - x and y
    """
    grid_dict = dict(letter_id=[], x=[], y=[])
    grid_step = get_grid_step(letters_df, min_number_of_points_per_segment)

    for index, letter in letters_df.iterrows():
        for current_x in point_generator(Segment(letter.left, letter.right), grid_step):
            for current_y in point_generator(Segment(letter.lower, letter.upper), grid_step):
                grid_dict['letter_id'].append(letter.letter_id)
                grid_dict['x'].append(current_x)
                grid_dict['y'].append(current_y)

    return pd.DataFrame.from_dict(grid_dict), grid_step


def get_cluster_id(letter_id: int, grid_df: pd.DataFrame) -> int:
    """
    This function returns most frequent cluster id for current letter_id in grid_df
    :param letter_id: letter_id from letters_df
    :param grid_df: dataframe with columns letter_id, x, y, cluster_id
    :return: most common cluster id for current letter_id
    """
    all_cluster_ids_per_letter = grid_df[grid_df.letter_id == letter_id].cluster_id.values.reshape(-1)
    counter = Counter(all_cluster_ids_per_letter)

    return counter.most_common(1)[0][0]


def get_word_ids(letters_df: pd.DataFrame, min_number_of_points_per_segment: int) -> pd.DataFrame:
    """
    This functions finds word for each letter
    :param letters_df: this dataframe has letter_id, letter, left, right, lower and upper fields that stores:
    id of a letter,
    text information,
    left border of the current letter bounding box,
    right border of the current letter bounding box,
    lower border of the current letter bounding box,
    upper border of the current letter bounding box correspondingly
    :param min_number_of_points_per_segment:
    :return: copy of letters_df with additional column word_id
    """
    letters_df = letters_df.copy(deep=True)
    grid_df, grid_step = get_grid_df(letters_df, min_number_of_points_per_segment)
    clusterizer = DBSCAN(eps=2 * grid_step, metric='cityblock', min_samples=min_number_of_points_per_segment)
    grid_df['cluster_id'] = clusterizer.fit(grid_df.loc[:, ['x', 'y']]).labels_
    letters_df['word_id'] = letters_df.letter_id.apply(partial(get_cluster_id, grid_df=grid_df))

    return letters_df
