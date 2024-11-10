#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotkit import with_axes
from matplotkit.colors import get_colors

from multi_ruptures.api.stat import calculate_slope, include_start_end


@with_axes(figsize=(10, 4))
def plot_series(
    data: np.ndarray | pd.Series,
    breakpoints: Sequence[int],
    cmap_name: str = "tab10",
    line_kwargs: Optional[Dict[str, Any]] = None,
    bkp_kwargs: Optional[Dict[str, Any]] = None,
    ax: plt.Axes | None = None,
) -> None:
    """Plot a time series with breakpoints."""
    assert isinstance(
        ax, plt.Axes
    ), f"ax must be a matplotlib Axes instance, got {type(ax)}."
    colors = get_colors(len(breakpoints) + 1, cmap_name)
    # Plot data
    ax.plot(data, **(line_kwargs or {}))
    sequence = include_start_end(data, breakpoints)
    # Plot breakpoints
    for i, start in enumerate(sequence[:-1]):
        end = sequence[i + 1]
        slope = calculate_slope(data[start:end])
        ax.axvspan(
            start,
            end,
            color=colors[i],
            alpha=0.2,
            label=f"Segment {i + 1} (slope={slope:.2f})",
            **(bkp_kwargs or {}),
        )
    ax.legend()
    return ax
