#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from __future__ import annotations

from typing import Literal, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

import numpy as np
import pandas as pd
import ruptures as rpt

# Type definitions
VALMETHODS: TypeAlias = Literal["Dynp", "Binseg", "BottomUp", "Window"]
DEFAULT_MIN_SIZE: int = 5

ALGORITHMS = ["Dynp", "Binseg", "BottomUp", "Window"]


def detect_breakpoints(
    data: Union[pd.Series, np.ndarray],
    n_bkps: int = 1,
    algorithm: VALMETHODS = "Dynp",
    min_size: int = DEFAULT_MIN_SIZE,
) -> Union[list[pd.Timestamp], pd.Timestamp, list[int], int]:
    """Detect trend breakpoints in time series data.

    Implementation based on [ruptures](https://centre-borelli.github.io/ruptures-docs/).

    Args:
        series: Time series data with time index and values to analyze.
        n_bkps: Expected number of breakpoints (default: 1).
        algorithm: Choice of algorithm:
            - "Dynp": Dynamic programming
            - "Binseg": Binary segmentation
            - "BottomUp": Bottom-up segmentation
            - "Window": Sliding window
        min_size: Minimum segment size between breakpoints (default: 5).

    Returns:
        If n_bkps=1: Single timestamp of the breakpoint, or None if not found.
        If n_bkps>1: List of breakpoint timestamps, or empty list if none found.

    Raises:
        ValueError: If algorithm is invalid or parameters are out of range.
    """
    if not isinstance(n_bkps, int) or n_bkps < 1:
        raise ValueError("Number of breakpoints must be positive integer.")
    # Convert pd.Series to np.ndarray if necessary
    if isinstance(data, pd.Series):
        is_series = True
        index = data.index
        data = data.values
    else:
        is_series = False

    result = _breakpoints_index(
        data=data, n_bkps=n_bkps, algorithm=algorithm, min_size=min_size
    )
    breakpoints = [index[i] for i in result[:-1]] if is_series else result[:-1]
    return breakpoints[0] if n_bkps == 1 and breakpoints else breakpoints


def _breakpoints_index(
    data: np.ndarray,
    n_bkps: int,
    algorithm: str = "Dynp",
    min_size: int = DEFAULT_MIN_SIZE,
) -> list[int]:
    """Internal function to compute breakpoint indices."""
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Algorithm must be one of {ALGORITHMS}, got {algorithm}")

    algo = getattr(rpt, algorithm)(model="l2", min_size=min_size)
    algo.fit(data)
    return algo.predict(n_bkps=n_bkps)
