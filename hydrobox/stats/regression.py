"""Regression Module

Common tools for calculating linear regression and produce scatter plots.

"""
from itertools import product

from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np

from hydrobox.toolbox import merge


def linear_regression(*x, df=None, plot=False, ax=None, notext=False):
    """Linear Regression tool

    This tool can be used for a number of regression related tasks. It can
    calculate a linear regression between two observables and also return a
    scatter plot including the regression parameters and function.

    In case more than two ``Series`` or ``arrays`` are passed, they will be
    merged into a ``DataFrame`` and a linear regression between all
    combinations will be calculated and potted if desired.

    Parameters
    ----------
    x : pandas.Series, numpy.ndarray
        If df is None, at least two Series or arrays have to be passed. If
        more are passed, a multi output will be produced.
    df : pandas.DataFrame
        If df is set, all x occurrences will be ignored. DataFrame of the
        input to be used for calculating the linear regression,
        This attribute can be useful, whenever a multi input to x does not
        get merged correctly. Note that linear_regression will only use the
        DataFrame.data array and ignore all other structural elements.
    plot : bool
        If True, the function will output a matplotlib Figure or plot into an
        existing instance. If False (default) the data used for the plots
        will be returned.
    ax : matplotlib.Axes.Axessubplot
        Has to be a single matplotlib Axes instance if two data sets are
        passed or a list of Axes if more than two data sets are passed.
    notext : bool
        If True, the output of the fitting parameters as a text into the plot
        will be suppressed. This setting is ignored, is plot is set to False.

    Returns
    -------
    matplotlib.Figure
    numpy.ndarray

    Notes
    -----

    If plot is True and ax is not None, the number of passed Axes has to match
    the total combinations between the data sets. This is

    .. math:: N^2

    where N is the length of x, or the length of df.columns.

    .. warning::

        This function does just calculate a linear regression. It handles a
        multi input recursively and has some data wrangling overhead. If you are
        seeking a fast linear regression tool, use the scipy.stats.linregress
        function directly.

    """
    # combine all inputs
    if df is None:
        df = merge(*x, dropna=False)

    if len(df.columns) == 2:
        slope, intercept, rvalue, pvalue, stderr = linregress(df.values[:, 0],
                                                              df.values[:, 1])

        # calculate regression
        reg = dict(slope=slope, intercept=intercept, rvalue=rvalue,
                   pvalue=pvalue, stderr=stderr)

        # return data
        if not plot:
            return reg

        # return plot
        else:   # pragma: no cover
            # build the ax if necessary
            if ax is None:
                fig, ax = plt.subplots(1, 1, figsize=(6, 6))
            else:
                fig = ax.get_figure()

            ax.scatter(df.values[:, 0], df.values[:, 1], 25, marker='.',
                       color='blue')
            if not notext:
                ax.text(0.05, 0.95,
                        '\n'.join(
                            ['%s: %.2f' % (k, v) for k, v in reg.items()]),
                        ha='left', va='top', transform=ax.transAxes
                        )
            x = df.values[:, 0]
            y = x * reg['slope'] + reg['intercept']
            ax.plot(x, y, '-g')

            return fig

    # more than two are given, call recursively
    else:
        # get the number of data sets
        n = len(df.columns)

        # create a plot
        if plot:    # pragma: no cover
            if ax is None:
                fig, axes = plt.subplots(n, n, figsize=(n * 5, n * 5),
                                         sharex=True, sharey=True)
            else:
                axes = ax
                fig = axes.flatten()[0].get_figure()
            # make sure there are enough AxesSubplots
            assert len(axes.flatten()) == n * n

            # call linear regression for all combinations
            for i, col_names in zip(
                    range(n * n),
                    product(df.columns, df.columns)
            ):
                if col_names[0] == col_names[1]:
                    # TODO: as soon as implemented, use the histogram tool here
                    continue
                linear_regression(df=df[[*col_names]],
                                  plot=True, ax=axes.flatten()[i],
                                  notext=notext)

            # return the whole figure
            plt.tight_layout()
            return fig

        else:
            p = product(df.columns, df.columns)

            # define a sorting function
            # before the .values method of the resulting dictionary was used,
            # but Python 3.5 and 3.6 return the dictionary with a different
            # order. therefore a explicit sorting function is needed
            def to_array(d):
                return [d['slope'], d['intercept'], d['rvalue'],
                        d['pvalue'], d['stderr']]

            # old function, kept for reference
            # to_array = lambda d: np.array(list(d.values()))
            res = [to_array(linear_regression(df[[*n]])) for n in p]

            # build the results
            np_res = [np.array(el).reshape((n, n)) for el in zip(*res)]
            for el in np_res:
                np.fill_diagonal(el, np.NaN)

            # extract and return
            slope, intercept, rvalue, pvalue, stderr = np_res
            return slope, intercept, rvalue, pvalue, stderr
