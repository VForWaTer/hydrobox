"""
Common tools for diagnosic tools frequently used in catchment hydrology.

"""
from typing import Union, Optional, Any
from matplotlib.axes import SubplotBase
from matplotlib.pyplot import Figure
import numpy as np
import pandas as pd
from datetime import datetime
from scipy.stats import rankdata

from hydrobox.plotting import plot_function_loader


def flow_duration_curve(
        x: Union[np.ndarray, pd.Series], 
        log: bool = True, 
        plot: bool = True, 
        non_exceeding:bool = True, 
        ax: Optional[Union[SubplotBase, Any]] = None, 
        **kwargs
    ) -> Union[np.ndarray, Figure]:
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
    ax : matplotlib.AxesSubplot | bokeh.Figure , default=None
        if not None, will plot into that AxesSubplot or Figure instance.
        .. note::
            If you pass an object, be sure to set the correct plotting 
            backend first.
    kwargs : kwargs,
        will be passed to the ``matplotlib.pyplot.plot`` function

    Returns
    -------
    matplotlib.Figure :
        if `plot` was `True`
    numpy.ndarray :
        if `plot was `False`

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
    else:
        pfunc = plot_function_loader('flow_duration_curve')
    
    fig = pfunc(func_args=dict(
        x=x[index], 
        y=p[index], 
        non_exceeding=non_exceeding,
        log=log,
        figure=ax),
        plot_args=kwargs
    )
    return fig


def regime(x, percentiles=None, normalize=False, agg='nanmedian', plot=True,
           ax=None, cmap='blues', **kwargs):
    r"""Calculate hydrological regime

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
    percentiles : int, list, numpy.ndarray, default=None
        percentiles can be used to calculate percentiles along with the main
        aggregate. The percentiles can either be set by an integer or a list.
        If an integer is passed, that many percentiles will be evenly spreaded
        between the 0th and 100th percentiles. A list can set the desired
        percentiles directly.
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
    cmap : string, optional
        Specify a colormap for generating the Percentile areas is a smooth
        color gradient. This has to be a valid 
        `colorcet colormap reference <https://colorcet.holoviz.org/user_guide/Continuous.html>`_.
        Defaults to ``'Blue'``.
    color : string, optional
        Define the color of the main aggregate. If ``None``, the first color
        of the specified cmap will be used.
    lw : int, optinal
        linewidth parameter in pixel. Defaults to 3.
    linestyle : string, optional
        Any valid matplotlib linestyle definition is accepted.

            ``':'``    -  dotted

            ``'-.'``   -  dash-dotted

            ``'--'``   -  dashed

            ``'-'``    -  solid


    Returns
    -------
    matplotlib.Figure :
        if `plot` was `True`
    pandas.DataFrame :
        if `plot` was `False` and `quantiles` are not None
    numpy.ndarray :
        if `plot` was `False` and `quantiles` is None

    Notes
    -----

    In case the color argument is not passed it will default to the first
    color in the the specified colormap (cmap). You might want to overwrite
    this in case no percentiles are produced, as many colormaps range from
    light to dark colors and the first color might just default to while.

    """
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('Data has to be indexed by a pandas.DatetimeIndex.')

    # create the percentiles
    if isinstance(percentiles, int):
        percentiles = np.linspace(0, 100, percentiles + 1, endpoint=False)[1:]

    if callable(agg):
        f = agg
    else:
        try:
            f = getattr(np, agg)
        except AttributeError:
            raise ValueError('The function %s cannot be imported from numpy')

    # create month index
    idx = [int(datetime.strftime(_, '%m')) for _ in x.index]

    # aggregate the regime and set the index
    if isinstance(x, pd.Series):
        x = pd.DataFrame(index=x.index, data=x.values)
    df = x.groupby(idx).aggregate(f)
    df.set_index(np.unique(idx), inplace=True)

    # build percentiles
    if percentiles is not None:
        for q in percentiles:
            df['q%d' % q] = x.groupby(idx).aggregate(
                lambda v: np.nanpercentile(v, q))

    # handle normalize
    if normalize:
        for col in df.columns:
            df[col] = df[col] / f(df[col])

    if not plot:
        if len(df.columns) == 1:
            return df.values
        else:
            return df
    else:
        pfunc = plot_function_loader('regime')

    # check if a colormap was set
    fig = pfunc(
        func_args=dict(df=df, figure=ax, cmap=cmap),
        plot_args=kwargs
    )

    return fig
