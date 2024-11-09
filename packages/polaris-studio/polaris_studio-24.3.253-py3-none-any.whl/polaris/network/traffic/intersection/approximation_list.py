# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
from typing import List, Tuple

import numpy as np

from polaris.network.traffic.intersection.approximation import Approximation


def sort_approx_list(approximations: List[Approximation]):
    data_list, idx, theta = pure_list_sorting(approximations)
    theta = theta[idx] + 180
    diff = list(theta[1:] - theta[:-1])
    diff.append(360 - theta[-1] + theta[0])

    if max(diff) != diff[-1]:
        position = diff.index(max(diff)) + 1
        data_list = data_list[position:] + data_list[:position]
    incoming = [inc for inc in data_list if inc.function == "incoming"][::-1]
    outgoing = [inc for inc in data_list if inc.function == "outgoing"]
    return incoming, outgoing


def pure_list_sorting(approximations: List[Approximation]) -> Tuple[List[Approximation], np.ndarray, np.ndarray]:
    direc = 1 if approximations[0].function == "outgoing" else -1
    direc *= 1 if approximations[0].direction == 0 else -1
    direc = direc if direc == -1 else 0
    node_coords = approximations[0].geo.coords[direc]
    zero = np.array(node_coords)
    arr = []
    for approx in approximations:  # type: Approximation
        if approx.geo.coords[0] == node_coords:
            point1 = np.array(approx.geo.coords[1]) - zero
        else:
            point1 = np.array(approx.geo.coords[-2]) - zero
        arr.append(point1)
    array = np.array(arr)
    yr = array[:, 1]
    xc = array[:, 0]
    center_xc = 0
    center_yr = 0
    theta = np.arctan2(yr - center_yr, xc - center_xc) * 180 / np.pi
    idx = np.argsort(theta)
    data_list = [approximations[x] for x in idx]
    return (data_list, idx, theta)
