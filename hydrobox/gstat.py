"""

"""
import numpy as np
import matplotlib.pyplot as plt

from skgstat import Variogram


def variogram_model(
        coordinates,
        values,
        effective_range,
        sill,
        nugget=0,
        n_lags=15,
        binning='even',
        maxlag='median',
        model='spherical',
        estimator='cressie',
        s=None,
        plot=True,
        ax=None
):
    """Variogram Function

    Calculate a variogram from the given parameters. This function will not
    fit the theoretical function to the experimental function, but use the
    passed arguments.

    Parameters
    ----------
    coordinates : numpy.ndarray
        List of n-dimensional coordinates. Refer to scikit-gstat for more
        information of this parameter.
    values : numpy.ndarray
        1D-array of observaitons. Has to match the length of the first axis
        of coordinates. Refer to scikit-gstat for more information of this
        parameter.
    effective_range : float
        Effective range of the theoretical model function. Refer to
        scikit-gstat for more information of this parameter.
    sill : sill
        Sill of the theoretical model function. Refer to scikit-gstat for
        more information of this parameter.
    nugget : float
        Nugget of the theoretical model function. Defaults to 0 (no nugget
        effect included in the model). Refer to scikit-gstat for more
        information of this parameter.
    n_lags : int
        Number of lag classes to be derived for the variogram. Refer to
        scikit-gstat for more information of this parameter.
    binning : str
        Method used for calculating the lag class edges. Can be either 'even'
        (default) or 'uniform'. 'even' will yield lag classes of same width,
        'uniform' will assure a uniform distribution across all lag classes.
        Refer to scikit-gstat for more information of this parameter.
    maxlag : float, str, None
        Maximum separating distance, at which a point pair will still be
        included into the variogram. Can be the number itself (float > 1),
        the share of the maximum separating distance observed (0 < maxlag <
        1), or one of 'mean', 'median' to calculate the mean or median of all
        separating distances as maxlag.
    model : str
        The theoretical variogram model. Can be one of:

            * spherical

            * exponential

            * gaussian

            * cubic

            * stable

            * matern

        Refer to scikit-gstat for more information of this parameter.
    estimator : str
        The semi-variance estimator to be used for the experimental
        variogram. Can be one of:

            * materon

            * cressie

            * dowd

            * genton

            * entropy

        Refer to scikit-gstat for more information of this parameter.
    s : float
        In case the model was set to matern, s is the smoothness parameter of
        the model. In case the model was set to stable, s is the shape
        parameter of the model. In all other cases, s will be ignored.
    plot : bool
        If True, the function will return a plot of the Variogram, if False,
        it will return a tuple of (bins, experimental, model).
    ax : None, matplotlib.AxesSubplot
        If None, the function will create a new matplotlib Figure. In case an
        AxesSubplot is passed, that instance will be used for plotting.

    Returns
    -------
    plot : matlotlib.Figure
        Will return a matplotlib Figure, if plot was set to True
    data : tuple
        Will return the tuple (bins, experimental, model) if plot was set to
        False.
    """
    V = Variogram(coordinates=coordinates, values=values,
                  estimator=estimator, model=model, maxlag=maxlag,
                  n_lags=n_lags, bin_func=binning, normalize=False)

    # get the experimental variogram
    _bins = V.bins
    _exp = V.experimental

    # align the model input
    _x = np.linspace(_bins[0], _bins[-1], 100)

    # build the coeffs
    cof = [effective_range, sill]
    if V.model.__name__ in ('matern', 'stable'):
        cof.append(s)
    cof.append(nugget)

    def modelf(x):
        return V.model(x, *cof)

    _y = np.fromiter(map(modelf, _x), dtype=float)

    # plot or return
    if not plot:
        return _bins, _exp, _y
    else:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        else:
            fig = ax.get_figure()

        # plot
        ax.plot(_bins, _exp, 'Dr')
        ax.plot(_x, _y, '-g')
        ax.set_xlabel('Lag')
        ax.set_ylabel('semi-variance [%s]' % estimator)
        ax.set_title('%s variogram' % model)

        return fig
