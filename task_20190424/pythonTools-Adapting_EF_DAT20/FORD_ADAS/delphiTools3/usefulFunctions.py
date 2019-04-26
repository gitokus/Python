import numpy as np


def get_consecutive(array, max_gap=2, col_num=0):
    """
    Find consecutive numbers in an array - especially useful if analyzing more than one event in log

    :param array: array object
    :param max_gap: maximum difference between numbers to treat them as consecutive
    :param col_num: number of column containing frames(only for 2D arrays)
    :return: list of split arrays
    """
    if array.ndim == 1:
        return np.split(array, np.where(np.diff(array) > max_gap)[0] + 1)
    else:
        return np.split(array, np.where(np.diff(array[:, col_num]) > max_gap)[0] + 1)