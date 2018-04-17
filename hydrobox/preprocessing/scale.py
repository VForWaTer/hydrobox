"""
The scale module combines low-level aggregation functionality for time series
data. The single functions operate on single time series instances.
All functions aiming on aggregating multi-dimensional data or multiple time
series are have a preceding 'm' in their function name.
"""
import numpy as np
import pandas as pd
from datetime import datetime


def aggregate(x, by, func=np.nanmean):
    """
    Time series aggregation
    -----------------------
    This function version will only operate on a single :class:`pandas.Series`.
    It has to be indexed by a `pandas.DatetimeIndex`. It aggregated to the
    given frequency by passing a `pandas.Grouper` conform string argument
    specifying the desired period like: '1M' for one month or '3Y-Sep' for
    three years starting at the first of October.


    Parameter
    ---------
    :param x: `pandas.Series`, the input data
    :param by:
    :param func:
    :return:
    """
    # check for being a time series
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    return x.groupby(pd.Grouper(freq=by)).aggregate(func)



def cut(x, start, stop):
    """
    Truncate Time series
    --------------------
    Truncates a :class:`pandas.Series` to the given period.
    The start and stop parameter need to be either a string or a
    :class:`datetime.datetime`, which will then be converted.
    Returns the truncated time series.

    Parameter
    ---------
    :param x: :class:`pandas.Series`, the input data
    :param start: string, datetime, begin of truncation
    :param stop: string, datetime, stop of truncation
    :return: :class:`pandas.Series`
    """
    # check for being a time series
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    if isinstance(start, datetime):
        start = start.strftime('%Y%m%d%H%M%S')
    if isinstance(stop, datetime):
        stop = stop.strftime('%Y%m%d%H%M%S')

    return x[start:stop].copy()
