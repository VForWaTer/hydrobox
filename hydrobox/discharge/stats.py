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

@accept(x=np.ndarray,log=bool, plot=bool, non_exceeding=bool, ax=('None', SubplotBase))
def flow_duration_curve(x, log=True, plot=True, non_exceeding=True, ax=None, **kwargs):
    """
    Calculate and draw a flow duration curve from the discharge measurements.

    All oberservations will be ordered and the Weibull empirical probability will be calculated.
    The ordered probabilities are plotted as a flow duration curve.

    In case x.ndim > 1, the function will be called iterativly along axis 0.

    :param x:   numpy.ndarray of discharge measurements
    :param log:  bool, if True plot on loglog axis, ignored when plot is False
    :param plot: bool, if False not plotting, returning the result instead
    :param non_exceeding: bool, if true use non-exceeding probalilities
    :param ax: matplotlib Subplot object, if not None, will plot into that instance
    :param kwargs: will be passed to the matplotlib.pyplot.plot function
    :return:
    """
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


@accept(x=(pd.DataFrame, pd.Series),
        quantiles=('None', int, list, np.ndarray),
        normalize=bool,
        agg='callable',
        plot=bool,
        ax=('None', SubplotBase))
def regime(x, quantiles=None, normalize=False, agg=np.nanmedian, plot=True, ax=None, **kwargs):
    """
    Calculate a hydrologic regime from given :py:class:: `pandas.DataFrame` or :py:class:: `pandas.Series`. The index
    has to be of type :py:class:: `pandas.DatetimeIndex`.

    :param x:
    :param quantiles:
    :param normalize:
    :param agg:
    :param plot:
    :param ax:
    :return:
    """
    if not isinstance(x.index, pd.DatetimeIndex):
        raise ValueError('The data has to be indexed by a pandas.DatetimeIndex.')

    # create the percentiles
    if isinstance(quantiles, int):
        quantiles = np.linspace(0, 100, quantiles + 1, endpoint=False)[1:]

    # check if n - dimensional
    if isinstance(x, pd.DataFrame) and len(x.columns) > 1:
        raise NotImplementedError

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