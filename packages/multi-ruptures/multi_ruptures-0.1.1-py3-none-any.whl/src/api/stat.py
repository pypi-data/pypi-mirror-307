#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from __future__ import annotations

from typing import List, Sequence

import numpy as np
import pandas as pd
import scipy.stats as stats


def calculate_slope(series: pd.Series | np.ndarray) -> float:
    """Calculate the linear growth rate (slope) of a series."""
    if len(series) <= 1:
        return 0
    x = np.arange(len(series))
    slope, _, _, _, _ = stats.linregress(x, series)
    return slope


def include_start_end(
    data: pd.Series | np.ndarray,
    breakpoints: Sequence[int],
) -> List[int]:
    """Include the start and end of the series in the breakpoints."""
    if isinstance(data, pd.Series):
        return [data.index[0], *breakpoints, data.index[-1]]
    if isinstance(data, np.ndarray):
        return [0, *breakpoints, len(data) - 1]
    raise ValueError("Unsupported data type")
