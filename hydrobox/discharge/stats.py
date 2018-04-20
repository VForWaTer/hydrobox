"""
Tools for extreme value statistics on discharge measurements.

"""
from hydrobox.utils.decorators import accept
from matplotlib.axes import SubplotBase
from matplotlib.pylab import get_cmap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import rankdata

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


@accept(x=(np.ndarray, pd.Series),log=bool, plot=bool, non_exceeding=bool,
ax=('None', SubplotBase))
def flow_duration_curve(x, log=True, plot=True, non_exceeding=True, ax=None, **kwargs):
    """Calculate a flow duration curve

    Calculate flow duration curve from the discharge measurements. The
    function can either return a ``matplotlib`` plot or return the ordered (
    non)-exceeding probabilities of the observations. These values can then
    be used in any external plotting environment.

    In case x.ndim > 1, the function will be called iteratively along axis 0.

    Parameters
    ----------
    x :   numpy.ndarray, pandas.Series
        Series of prefereably discharge measurements
    log :  bool, default=True
        if `True` plot on loglog axis, ignored when plot is `False`
    plot : bool, default=True
        if `False` plotting will be suppressed and the resulting array will
        be returned
    non_exceeding : bool, default=True
        if `True` use non-exceeding probabilities
    ax : matplotlib.AxesSubplot, default=None
        if not None, will plot into that AxesSubplot instance
    kwargs : kwargs,
        will be passed to the ``matplotlib.pyplot.plot`` function

    Returns
    -------
    matplotlib.AxesSubplot : if `plot` was `True`
    numpy.ndarray : if `plot was `False`

    Notes
    -----
    The probabilities are calculated using the Weibull empirical probability.
    Following [1]_, this probability can be calculated as:

    .. math:: p =m/(n + 1)

    where `m` is the rank of an observation in the ordered time series and
    `n` are the total observations. The increasion by one will prevent 0%
    and 100% probabilities.

    References
    ----------
    ..  [1] Sloto, R. a., & Crouse, M. Y. (1996). Hysep: a computer program
        for streamflow hydrograph separation and analysis. U.S. Geological
        Survey Water-Resources Investigations Report, 96(4040), 54.

    """
    # omit the Series index
    if isinstance(x, pd.Series):
        x = x.values

    # if x has more than one dimension call this func recursive along axis=0
    if x.ndim > 1:
        # check if plot was None, then iterate along axis=0
        if not plot:
            return np.apply_along_axis(flow_duration_curve, 0, x, non_exceeding=non_exceeding, plot=False)
        else:
            # plot, if ax is None, create
            if ax is None:
                fig, ax = plt.subplots(1,1)
            last_ax = list(map(lambda x: flow_duration_curve(x, log=log, non_exceeding=non_exceeding, ax=ax), x.T))[-1]
            return last_ax

    # calculate the ranks
    ranks = rankdata(x, method='average')

    # calculate weibull pdf
    N = x.size

    # calculate probabilities
    p = np.fromiter(map(lambda r: r / (N + 1), ranks), dtype=np.float)

    # create sorting index
    if non_exceeding:
        index = np.argsort(p)
    else:
        index = np.argsort(p)[::-1]

    if not plot:
        return p[index]

    # generate an Axes, if ax is None
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    # plot
    # set some defaults
    kwargs.setdefault('linestyle', '-')
    kwargs.setdefault('color', 'b')
    ax.plot(x[index], p[index], **kwargs)

    # label
    ax.set_xlabel('discharge [m3/s]')
    ax.set_ylabel('%sexceeding prob.' % ('non-' if non_exceeding else ''))

    # handle loglog
    if log:
        ax.loglog()
    else:
        ax.set_ylim((-0.05, 1.1))
        ax.set_xlim(np.nanmin(x) * 0.98, np.nanmax(x) * 1.02)
    ax.set_title('%sFDC' % ('loglog ' if log else ''))
    ax.grid(which='both' if log else 'major')

    return ax


@accept(x=pd.Series,
        quantiles=('None', int, list, np.ndarray),
        normalize=bool,
        agg=str,
        plot=bool,
        ax=('None', SubplotBase))
def regime(x, quantiles=None, normalize=False, agg='nanmedian', plot=True,
           ax=None, **kwargs):
    """Calculate hydrological regime

    Calculate a hydrological regime from discharge measurements. A regime is
    a annual overview, where all observations are aggregated across the
    month. Therefore it does only make sense to calculate a regime over more
    than one year with a temporal resolution higher than monthly.

    The regime can either be plotted or the calculated monthly aggreates can
    be returned (along with the quantiles, if any were calculated).

    Parameters
    ----------
    x : pandas.Series
        The ``Series`` has to be indexed by a ``pandas.DatetimeIndex`` and
        hold the preferably discharge measurements. However, the methods
        does also work for other observables, if `agg` is adjusted.
    quantiles : int, list, numpy.ndarray, default=None
        quantiles can be used to calculate quantiles along with the main
        aggregate. The quantiles can either be set by an integer or a list.
        If an integer is passed, that many quantiles will be evenly spreaded
        between the 0th and 100th quantile. A list can set the desired
        quantiles directly.
    normalize : bool, default=False
        If `True`, the regime will be normalized by the aggregate over all
        months. Then the numbers do not give the discharge itself, but the
        ratio of the monthly discharge to the overall discharge.
    agg : string, default='nanmedian'
        Define the function used for aggregation. Usually this will be
        'mean' or 'median'. If there might be `NaN` values in the
        observations, the 'nan' prefixed functions can be used. In general,
        any aggregating function, which can be imported from ``numpy`` can
        be used.
    plot : bool, default=True
        if `False` plotting will be suppressed and the resulting
        ``pandas.DataFrame`` will be returned. In case `quantiles` was None,
        only the regime values will be returned as `numpy.ndarray`
    ax : matplotlib.AxesSubplot, default=None
        if not None, will plot into that AxesSubplot instance

    Returns
    -------
    matplotlib.AxesSubplot : if `plot` was `True`
    pandas.DataFrame : if `plot` was `False` and `quantiles` are not None
    numpy.ndarray :   if `plot` was `False` and `quantiles` is None

    """
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    # create the percentiles
    if isinstance(quantiles, int):
        quantiles = np.linspace(0, 100, quantiles + 1, endpoint=False)[1:]

    try:
        agg = getattr(np, agg)
    except AttributeError:
        raise ValueError('The function %s cannot be imported from numpy')

    # create month index
    idx = [int(datetime.strftime(_, '%m')) for _ in x.index]

    # aggregate the regime and set the index
    df = x.groupby(idx).aggregate(agg)
    df.set_index(np.unique(idx), inplace=True)

    # build quantiles
    if quantiles is not None:
        for q in quantiles:
            df['q%d' % q] = x.groupby(idx).aggregate(lambda v: np.nanpercentile(v, q))

    # handle normalize
    if normalize:
        for col in df.columns:
            df[col] = df[col] / agg(df[col])

    if not plot:
        if len(df.columns) == 1:
            return df.values
        else:
            return df

    # create the plot
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    # some defaults
    kwargs.setdefault('cmap', 'Blues')
    kwargs.setdefault('lw', 3)
    kwargs.setdefault('linestyle', '-')

    cm = get_cmap(kwargs['cmap'])

    # check if there are quantiles
    if len(df.columns) > 1:
        # build the colormap
        n = int((len(df.columns) - 1) / 2)
        cmap = [cm(1. * _ / n) for _ in range(n)]
        cmap = np.concatenate((cmap, cmap[::-1]))

        # plot
        for i in range(len(df.columns) - 2, 1, -1):
            ax.fill_between(df.index, df.iloc[:, i], df.iloc[:, i -1], interpolate=True, color=cmap[i - 1])

    # plot the main aggregate
    ax.plot(df.index, df.iloc[:, 0], linestyle=kwargs['linestyle'], color=cm(0.0), lw=kwargs['lw'])
    ax.set_xlim(0, 12)
    plt.xticks(df.index, MONTHS, rotation=45)

    return ax