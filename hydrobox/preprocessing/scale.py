"""
The scale module combines low-level aggregation functionality for time series
data. The single functions operate on single time series instances.
All functions aiming on aggregating multi-dimensional data or multiple time
series are have a preceding 'm' in their function name.
"""
from datetime import datetime

import numpy as np
import pandas as pd

from hydrobox.utils.decorators import accept


@accept(x=(pd.Series, pd.DataFrame), by=str, func=(str, 'callable'))
def aggregate(x, by, func='nanmean'):
    """Time series aggregation

    This function version will only operate on a single ``pandas.Series`` or
    ``pandas.DataFrame`` instance. It has to be indexed by a `pandas.DatetimeIndex`. The input
    data will be aggregated to the given frequency by passing a `pandas.Grouper` conform string
    argument specifying the desired period like: '1M' for one month or '3Y-Sep' for three years
    starting at the first of October.


    Parameters
    ----------
    x: ``pandas.Series``, ``pandas.DataFrame``
        The input data, will be aggregated over the index.
    by : string
        Specifies the desired temporal resolution. Will be passed as ``freq`` argument of a
        ``pandas.Grouper`` object for grouping the data into the new resolution.
    func : string
        Function identifier used for aggregation. Has to be importable from ``numpy``. The
        function must accept n input values and aggregate them to only a single one.

    Returns
    -------
    pandas.Series :
        if x was of type ``pandas.Series``
    pandas.DataFrame :
        if c was of type ``pandas.DataFrame``

    """
    # check for being a time series
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    # get the function
    if callable(func):
        f = func
    else:
        try:
            f = getattr(np, func)
        except AttributeError:
            raise ValueError('The function %s cannot be imported. the aggregation function has \
                             to be importable from numpy.' % func)

    return x.groupby(pd.Grouper(freq=by)).aggregate(f)


@accept(
    x=(pd.Series, pd.DataFrame),
    start=(str, datetime, 'None'),
    stop=(str, datetime, 'None'))
def cut(x, start, stop):
    """Truncate Time series

    Truncates a ``pandas.Series`` or ``pandas.DataFrame`` to the given period. The start and
    stop parameter need to be either a string or a ``datetime.datetime``, which will then be
    converted. Returns the truncated time series.

    Parameters
    ----------
    x : ``pandas.Series``, ``pandas.DataFrame``
        The input data, will be truncated
    start : string, datetime
        Begin of truncation. Can be a ``datetime.datetime`` or a string. If a string is passed,
        it has to use the format 'YYYYMMDDhhmmss', where the time componen 'hhmmss' can be omitted.
    stop : string, datetime,
        End of truncation. Can be a ``datetime.datetime`` or a string. If a string is passed,
        it has to use the format 'YYYYMMDDhhmmss', where the time componen 'hhmmss' can be omitted.

    """
    # check for being a time series
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    if isinstance(start, datetime):
        start = start.strftime('%Y%m%d%H%M%S')
    if isinstance(stop, datetime):
        stop = stop.strftime('%Y%m%d%H%M%S')

    return x[start:stop].copy()
