"""
Geostatistics Package
=====================

The geostatistics package of hydrobox makes use of two other
great packages: GSTools and SciKit-GStat.

"""
import numpy as np
import skgstat as skg
import gstools as gs

from hydrobox.geostat import typing
from hydrobox.plotting import plot_function_loader

def variogram(
    coordinates: np.ndarray,
    values: np.ndarray,
    estimator: typing.Estimator = 'matheron',
    model: typing.Model = 'spherical',
    dist_func: typing.DistFunc = 'euclidean',
    bin_func: typing.BinFunc = 'even',
    fit_method: typing.FitMethod = 'trf',
    fit_sigma: typing.FitSigma = None,
    use_nugget: bool = False,
    maxlag: typing.Maxlag = None,
    n_lags: typing.Union[int, None] = None,
    plot: bool = False,
    plot_type: typing.Literal['plot', 'distance_difference', 'location_trend', 'scattergram'] = 'plot',
    **kwargs
) -> skg.Variogram:
    """
    """
    # create the variogram
    v = skg.Variogram(
        coordinates=coordinates,
        values=values,
        estimator=estimator,
        model=model,
        dist_func=dist_func,
        bin_func=bin_func,
        fit_method=fit_method,
        fit_sigma=fit_sigma,
        use_nugget=use_nugget,
        maxlag=maxlag,
        n_lags=n_lags,
        **kwargs
    )

    if not plot:
        return v
    
    # otherwise create a plot
    pfunc = plot_function_loader('variogram')
    fig = pfunc(func_args=dict(
        variogram=V,
        plot_type=plot_type
        ), plot_args=kwargs)
    return fig
