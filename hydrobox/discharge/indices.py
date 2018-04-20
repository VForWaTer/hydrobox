"""
Common indices frequently used to describe discharge measurements in a single
coefficient.

"""
import numpy as np
import pandas as pd

from hydrobox.utils.decorators import accept


@accept(x=(pd.Series, np.ndarray))
def richards_baker(x):
    r"""Richards-Baker Flashiness Index

    Calculates the Richards-Baker Flashiness index (RB Index), which is a
    extension of the Richards Pathlengh index. In contrast to the Pathlength
    of a signal, the R-B Index is relative to the total discharge and
    independend of the chosen unit.

    Parameters
    ----------
    x : numpy.ndarray, pd.Series
        The discharge input values.

    Returns
    -------
    numpy.ndarray

    Notes
    -----
    The Richards-Baker Flashiness Index [2]_ is defined as:

    .. math::

        {RBI} = \frac{\sum_{i=1}^{n}|q_i - q_{i-1}|}{\sum_{i=1}^{n} q_i}



    References
    ----------
    ..  [2] Baker D.B., P. Richards, T.T. Loftus, J.W. Kramer. A new
        flashiness index: characteristics and applications to midwestern
        rivers and streams. JAWRA Journal of the American Water Resources
        Association, 40(2), 503-522, 2004.

    """
    # convert Series
    if isinstance(x, pd.Series):
        x = x.values

    nominator = np.sum(np.fromiter(
        (np.abs(x[i] - x[i -1]) for i in range(1,len(x))),
        dtype=x.dtype))

    return nominator / np.sum(x[1:])
