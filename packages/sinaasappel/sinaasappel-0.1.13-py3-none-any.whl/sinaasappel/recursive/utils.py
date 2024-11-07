import typing as t

import numpy as np


def recursive_sum(elem: t.Union[int, list[t.Union[int, list]]]):
    """"""
    if type(elem) is int:
        return elem
    return numpy_sum([recursive_sum(subelem) for subelem in elem])


def numpy_sum(elem: list[int]):
    return np.sum(elem)


def non_numpy_sum(elem: list[int]):
    return sum(elem)
