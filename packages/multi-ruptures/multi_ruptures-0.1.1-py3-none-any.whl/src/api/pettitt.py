#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np
import pandas as pd
from pyhomogeneity import pettitt_test


def _iterative_pettitt_index(
    data: np.ndarray,
    alpha: float = 0.05,
    sim: int = 20000,
    min_size: Optional[int] = None,
) -> list[int]:
    """Internal function, returns the index of breakpoints."""
    change_points = []
    length = len(data)
    segments = [(0, length)]
    if min_size is None:
        min_size = length // 5

    while segments:
        new_segments = []
        for start, end in segments:
            segment = data[start:end]
            if len(segment) < min_size * 2:
                continue

            h, cp, _, _, _ = pettitt_test(segment, alpha, sim)

            if h:
                abs_cp = start + cp
                if (abs_cp - start >= min_size) and (end - abs_cp >= min_size):
                    change_points.append(int(abs_cp))
                    new_segments.append((start, abs_cp))
                    new_segments.append((abs_cp, end))

        segments = new_segments

    return sorted(change_points)


def iterative_pettitt(
    data: Sequence | pd.Series,
    alpha: float = 0.05,
    sim: int = 20000,
    min_size: Optional[int] = None,
) -> list[pd.Timestamp] | list[int]:
    """Iteratively perform Pettitt test until no significant breakpoints are found.

    Args:
        data:
            Input data, can be a list, array, or pandas.Series
        alpha:
            Significance level, default 0.05
        sim:
            Number of simulations, default 20000
        min_size:
            Minimum segment length, defaults to 1/5 of data length.
            Stops further segmentation when segment length is less than this value.

    Returns:
        List of breakpoints (timestamps if input is pd.Series, indices otherwise)
    """
    # 处理输入数据
    if isinstance(data, pd.Series):
        index = data.index
        data = data.values
        breakpoints = _iterative_pettitt_index(data, alpha, sim, min_size)
        return [index[i] for i in breakpoints]

    data = np.array(data)
    return _iterative_pettitt_index(data, alpha, sim, min_size)
