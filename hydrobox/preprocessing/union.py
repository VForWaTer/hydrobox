"""
Collects convenient methods for combining multiple data sets into a single one.
This is typically a pandas.DataFrame then.
"""
import pandas as pd


def merge(*x, dropna=False):
    r"""Merge multiple data sets.

    This method is a general tool for combining multiple data sources into a
    single structure. It can be used as a preprocessing step in case the next
    chained tool does only accept a single input data set, but can handle
    multi-dimensional data.
    For conveniently wrapping around a single dimension data set, it will
    return x as it is if len(x) == 1.

    Parameters
    ----------
    x : pd.Series
        Input series. All series have to share an Index. If the type of the
        index is different, a ValueError will be raised. In case an Index
        value is missing on one of the Series, it will be filled with a NaN
        value.
    dropna : bool, optional
        If dropna is True, all indices with at least **one** NaN will be
        dropped.

    Returns
    -------
    pandas.DataFrame

    Notes
    -----

    At the current state merge does only accept ``pandas.Series``.
    A ``pandas.DataFrame`` with len(x) columns is returned.

    """
    # check if only one series was passed
    if len(x) == 1:
        return x[0]
    elif len(x) == 0:
        return None

    # convert x from tuple to list
    x = list(x)

    # check the indices to be of same kind.
    dtype = type(x[0].index)
    if not all([isinstance(series.index, dtype) for series in x]):
        raise ValueError(
            'At least one data set was not of type %s.' % str(dtype))

    # build the first DataFrame
    df = pd.concat(x, axis=1)

    # if dropna was given, remove NaN values
    if dropna:
        df.dropna(axis=0, how='any', inplace=True)

    return df
