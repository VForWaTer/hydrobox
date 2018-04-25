"""Rolling statistics

Helper functions to apply rolling statistics to input data.

"""
from hydrobox.utils.decorators import accept
import pandas as pd
import numpy as np

@accept(
    x=(pd.Series, pd.DataFrame),
    window_size=int,
    window_type=(str, 'None'),
    func=(str, 'callable'))
def moving_window(x, window_size=5, window_type=None, func='nanmean'):
    r"""Moving window statistics

    Applies a moving window function to the input data. Each of the grouped
    windows will be aggregated into a resulting time series.

    Parameters
    ----------
    x : ``pandas.Series``, ``pandas.DataFrame``
        Input data. The data should have a ``pandas.DatetimeIndex`` in order
        to produce meaningful results. However, this is not needed and will
        technically work on different indexed data.
    window_size : int
        The specified number of values will be grouped into a window. This
        parameter might have different behavior in case the window_type is
        not `None`.
    window_type : str, default=None
        If `None`, an even spaced window will be used and shifted by one for
        each group. Else, a window constructing class can be specified.
        Possible constructors are specified in ``pandas.DataFrame.rolling``.
    func : str
        Aggregating function for calculating the new window value. It has to
        be importable from ``numpy``, accept various input values and return
        only a single value like ``numpy.std`` or ``numpy.median``.

    Returns
    -------
    pandas.Series
    pandas.DataFrame

    Notes
    -----

    Be aware that most window types (if window_type is not None) do only
    work with either ``numpy.sum`` or ``numpy.mean``.

    Furthermore, most windows cannot work with the 'nan' versions of
    numpy aggregating function. Therefore in case window_type is None, any
    'nan' will be removed from the func string. In case you want to force this
    behaviour, wrap the numpy function into a ``lambda``.

    Examples
    --------
    This way, you can prevent the replacement of a np.nan* function:

    >>> moving_window(x, func=lambda x: np.nanmean(x))
    array([NaN, NaN, NaN, 4.7445, 4.784 ... 6.34532])

    """
    # remove NaNs from the function name if a window_type was set
    if window_type is not None and isinstance(func, str):
        func = func.replace('nan', '')

    # get the function or load it from numpy
    if callable(func):
        f = func
    else:
        try:
            f = getattr(np, func)
        except AttributeError:
            raise ValueError(
                'The function %s cannot be imported from numpy.' % func)

    # apply and return
    try:
        return x.rolling(window=window_size, win_type=window_type).aggregate(f)
    except AttributeError as e:
        raise AttributeError('This did not work. Maybe the func %s is not \
                             allowed for this window type?\n original Error: \
                             %s.' % (func, str(e)))
