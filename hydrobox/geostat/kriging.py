from typing import List, Union, Literal
import numpy as np
import skgstat as skg
import plotly.graph_objects as go

from hydrobox.plotting import plot_function_loader

def _kriging(
    variogram: skg.Variogram,
    grid_resolution = None,
    return_type = 'plot',
    plot_kwargs = {},
    **kwargs
) -> Union[List[np.ndarray], go.Figure]:
    """
    Actual interface to gstools
    """
    # get the kriging class
    krige = variogram.to_gs_krige(**kwargs)

    if return_type == 'object':
        return krige

    # build the grid
    if isinstance(grid_resolution, int):
        # get the coordinate ranges
        lower = np.min(variogram.coordinates, axis=0)
        upper = np.max(variogram.coordinates, axis=0)
        dims = [np.linspace(l, u, grid_resolution) for l, u in zip(lower, upper)]
    else:
        raise AttributeError('Right now, only integer grid_resolutions are supported.')

    # call structured
    field, sigma = krige.structured(dims)

    if return_type == 'grid':
        return (field, sigma)
    
    # return the plot
    if field.ndim > 2:
        raise ValueError('Plotting not supported for dim > 2.')

    pfunc = plot_function_loader('kriging')
    fig = pfunc(
        func_args=dict(
            variogram=variogram,
            field=field,
            sigma=sigma
        ),
        plot_args=plot_kwargs
    )

    return fig


def ordinary_kriging(
    variogram: skg.Variogram,
    grid_resolution: int,
    exact: bool = True,
    cond_err: Union[Literal['nugget'], float, list] = 'nugget',
    pseudo_inv: bool = True,
    pseudo_inv_type: Literal['pinv', 'pinv2', 'pinvh'] = 'pinv',
    return_type: Literal['object', 'plot', 'grid'] = 'plot',
    **kwargs
) -> Union[List[np.ndarray], go.Figure]:
    """
    Use a scikit-gstat :class:`Variogram <skgstat.Variogram>` to estimate
    spatial properties of a sample. Uses this variogram to interpolate
    using kriging. The Kriging is done with the
    :class:`Ordinary <gstools.krige.Ordinary>` class. Refer to the docs
    of :class:`Ordinary <gstools.krige.Ordinary>` to learn about the
    parameters.

    .. note::
        Right now, there are only very limited possibilities to specify
        an interpolation grid. Only setting the resolution of the result
        like: ``50x50`` is possible by passing the integer ``50``.
        More fine-grained control will be added with a future release.

    Parameters
    ----------
    variogram : skgstat.Variogram
        Variogram used for kriging
    grid_resolution : int
        Resoultion of the interpolation grid. The resolution will be used
        in all input data dimensions, which can lead to non-quadratic
        grid cells.
    exact : bool
        If True (default), the input data will be matched exactly.
        Refer to :class:`Ordinary <gstools.krige.Ordinary>` 
        for more info.
    cond_err : str, float, list
        Measurement error, or variogram nugget.
        Refer to :class:`Ordinary <gstools.krige.Ordinary>` 
        for more info.
    pseudo_inv : bool
        If True, the Kriging is more robust, but also slower.
        Refer to :class:`Ordinary <gstools.krige.Ordinary>` 
        for more info.
    pseudo_inv_type : str
        Type of matrix inversion used if pseudo_inv is True.
        Refer to :class:`Ordinary <gstools.krige.Ordinary>` 
        for more info.
    return_type : str
        Specify how the result should be retuned. Can be the
        kriging class itself (``'object'``), the interpolated
        grid (``'grid'``) or a plot of the grid (``'plot'``).

    Returns
    -------
    results : numpy.ndarray, numpy.ndarray
        Interpolation grid and kriging error grid
    fig : plotly.graph_objects.Figure, matplotlib.Figure
        Figure of the result plot.

    """
    # build the kwargs
    args = dict(
        exact=exact,
        cond_err=cond_err,
        pseudo_inv=pseudo_inv,
        pseudo_inv_type=pseudo_inv_type
    )

    # return the results
    return _kriging(
        variogram=variogram,
        grid_resolution=grid_resolution,
        return_type=return_type,
        plot_kwargs=kwargs,
        **args
    )

def simple_kriging(
    variogram: skg.Variogram,
    grid_resolution: int,
    mean: float,
    exact: bool = True,
    cond_err: Union[Literal['nugget'], float, list] = 'nugget',
    pseudo_inv: bool = True,
    pseudo_inv_type: Literal['pinv', 'pinv2', 'pinvh'] = 'pinv',

    return_type: Literal['object', 'plot', 'grid'] = 'plot',
        **kwargs
) -> Union[List[np.ndarray], go.Figure]:
    """
    Use a scikit-gstat :class:`Variogram <skgstat.Variogram>` to estimate
    spatial properties of a sample. Uses this variogram to interpolate
    using kriging. The Kriging is done with the
    :class:`Simple <gstools.krige.Simple>` class. Refer to the docs
    of :class:`Simple <gstools.krige.Simple>` to learn about the
    parameters.

    For simple kriging you need to pass the real mean value of the
    field (not the sample) in order to work correctly. If that is not
    available, refer to :func:`ordinary_kriging <hydrobox.geostat.ordinary_kriging>`.

    .. note::
        Right now, there are only very limited possibilities to specify
        an interpolation grid. Only setting the resolution of the result
        like: ``50x50`` is possible by passing the integer ``50``.
        More fine-grained control will be added with a future release.

    Parameters
    ----------
    variogram : skgstat.Variogram
        Variogram used for kriging
    grid_resolution : int
        Resoultion of the interpolation grid. The resolution will be used
        in all input data dimensions, which can lead to non-quadratic
        grid cells.
    mean : float
        The mean value of the field, that has to be known a priori.
        If you pass bs here, you will interpolate bs.
    exact : bool
        If True (default), the input data will be matched exactly.
        Refer to :class:`Simple <gstools.krige.Simple>` 
        for more info.
    cond_err : str, float, list
        Measurement error, or variogram nugget.
        Refer to :class:`Simple <gstools.krige.Simple>`
        for more info.
    pseudo_inv : bool
        If True, the Kriging is more robust, but also slower.
        Refer to :class:`Simple <gstools.krige.Simple>`
        for more info.
    pseudo_inv_type : str
        Type of matrix inversion used if pseudo_inv is True.
        Refer to :class:`Simple <gstools.krige.Simple>`
        for more info.
    return_type : str
        Specify how the result should be retuned. Can be the
        kriging class itself (``'object'``), the interpolated
        grid (``'grid'``) or a plot of the grid (``'plot'``).

    Returns
    -------
    results : numpy.ndarray, numpy.ndarray
        Interpolation grid and kriging error grid
    fig : plotly.graph_objects.Figure, matplotlib.Figure
        Figure of the result plot.

    """
    # build the kwargs
    args = dict(
        mean=mean,
        exact=exact,
        cond_err=cond_err,
        pseudo_inv=pseudo_inv,
        pseudo_inv_type=pseudo_inv_type
    )

    # return the results
    return _kriging(
        variogram=variogram,
        grid_resolution=grid_resolution,
        return_type=return_type,
        plot_kwargs=kwargs,
        **args
    )


def universal_kriging(
    variogram: skg.Variogram,
    grid_resolution: int,
    drift_functions: Literal['linear', 'quadratic'],
    exact: bool = True,
    cond_err: Union[Literal['nugget'], float, list] = 'nugget',
    pseudo_inv: bool = True,
    pseudo_inv_type: Literal['pinv', 'pinv2', 'pinvh'] = 'pinv',

    return_type: Literal['object', 'plot', 'grid'] = 'plot',
        **kwargs
) -> Union[List[np.ndarray], go.Figure]:
    """
    Use a scikit-gstat :class:`Variogram <skgstat.Variogram>` to estimate
    spatial properties of a sample. Uses this variogram to interpolate
    using kriging. The Kriging is done with the
    :class:`Universal <gstools.krige.Universal>` class. Refer to the docs
    of :class:`Universal <gstools.krige.Universal>` to learn about the
    parameters.

    For universal kriging you need to specify the interal drift term of
    the field. Then, this auto-regression will be taken into account 
    for kriging. This is useful for fields, that acutally show a drift.
    If that is not the case, refer to 
    :func:`ordinary_kriging <hydrobox.geostat.ordinary_kriging>` or 
    :func:`ext_drift_kriging <hydrobox.geostat.ext_drift_kriging>` for
    external drifts.

    .. note::
        Right now, there are only very limited possibilities to specify
        an interpolation grid. Only setting the resolution of the result
        like: ``50x50`` is possible by passing the integer ``50``.
        More fine-grained control will be added with a future release.

    Parameters
    ----------
    variogram : skgstat.Variogram
        Variogram used for kriging
    grid_resolution : int
        Resoultion of the interpolation grid. The resolution will be used
        in all input data dimensions, which can lead to non-quadratic
        grid cells.
    drift_functions : str
        The drift function used to perform regression kriging on the
        values of the sample. Can be either ``'linear'`` or ``'quadratic'``.
        Polynomials of higher order are currently only supported, if you use
        :class:`Universal <gstools.krige.Universal>` directly.
    exact : bool
        If True (default), the input data will be matched exactly.
        Refer to :class:`Universal <gstools.krige.Universal>`
        for more info.
    cond_err : str, float, list
        Measurement error, or variogram nugget.
        Refer to :class:`Universal <gstools.krige.Universal>`
        for more info.
    pseudo_inv : bool
        If True, the Kriging is more robust, but also slower.
        Refer to :class:`Universal <gstools.krige.Universal>`
        for more info.
    pseudo_inv_type : str
        Type of matrix inversion used if pseudo_inv is True.
        Refer to :class:`Universal <gstools.krige.Universal>`
        for more info.
    return_type : str
        Specify how the result should be retuned. Can be the
        kriging class itself (``'object'``), the interpolated
        grid (``'grid'``) or a plot of the grid (``'plot'``).

    Returns
    -------
    results : numpy.ndarray, numpy.ndarray
        Interpolation grid and kriging error grid
    fig : plotly.graph_objects.Figure, matplotlib.Figure
        Figure of the result plot.

    """
    # build the kwargs
    args = dict(
        drift_functions=drift_functions,
        exact=exact,
        cond_err=cond_err,
        pseudo_inv=pseudo_inv,
        pseudo_inv_type=pseudo_inv_type
    )

    # return the results
    return _kriging(
        variogram=variogram,
        grid_resolution=grid_resolution,
        return_type=return_type,
        plot_kwargs=kwargs,
        **args
    )


def ext_drift_kriging(
    variogram: skg.Variogram,
    grid_resolution: int,
    ext_drift: np.ndarray,
    exact: bool = True,
    cond_err: Union[Literal['nugget'], float, list] = 'nugget',
    pseudo_inv: bool = True,
    pseudo_inv_type: Literal['pinv', 'pinv2', 'pinvh'] = 'pinv',

    return_type: Literal['object', 'plot', 'grid'] = 'plot',
        **kwargs
) -> Union[List[np.ndarray], go.Figure]:
    """
    Use a scikit-gstat :class:`Variogram <skgstat.Variogram>` to estimate
    spatial properties of a sample. Uses this variogram to interpolate
    using kriging. The Kriging is done with the
    :class:`ExtDrift <gstools.krige.ExtDrift>` class. Refer to the docs
    of :class:`ExtDrift <gstools.krige.ExtDrift>` to learn about the
    parameters.

    For external drift kriging you need to specify the external drift term of
    the field. Then, the regression between drift and sample will be taken 
    into account for kriging. This is useful for fields, that are actually 
    correlated to other fields, which are (more) available.
    If that is not the case, refer to 
    :func:`ordinary_kriging <hydrobox.geostat.ordinary_kriging>` for kriging
    without drift.

    .. note::
        Right now, there are only very limited possibilities to specify
        an interpolation grid. Only setting the resolution of the result
        like: ``50x50`` is possible by passing the integer ``50``.
        More fine-grained control will be added with a future release.

    Parameters
    ----------
    variogram : skgstat.Variogram
        Variogram used for kriging
    grid_resolution : int
        Resoultion of the interpolation grid. The resolution will be used
        in all input data dimensions, which can lead to non-quadratic
        grid cells.
    ext_drift : np.ndarray
        External drift values at the observation points
    exact : bool
        If True (default), the input data will be matched exactly.
        Refer to :class:`ExtDrift <gstools.krige.ExtDrift>`
        for more info.
    cond_err : str, float, list
        Measurement error, or variogram nugget.
        Refer to :class:`ExtDrift <gstools.krige.ExtDrift>`
        for more info.
    pseudo_inv : bool
        If True, the Kriging is more robust, but also slower.
        Refer to :class:`ExtDrift <gstools.krige.ExtDrift>`
        for more info.
    pseudo_inv_type : str
        Type of matrix inversion used if pseudo_inv is True.
        Refer to :class:`ExtDrift <gstools.krige.ExtDrift>`
        for more info.
    return_type : str
        Specify how the result should be retuned. Can be the
        kriging class itself (``'object'``), the interpolated
        grid (``'grid'``) or a plot of the grid (``'plot'``).

    Returns
    -------
    results : numpy.ndarray, numpy.ndarray
        Interpolation grid and kriging error grid
    fig : plotly.graph_objects.Figure, matplotlib.Figure
        Figure of the result plot.

    """
    # build the kwargs
    args = dict(
        ext_drift=ext_drift,
        exact=exact,
        cond_err=cond_err,
        pseudo_inv=pseudo_inv,
        pseudo_inv_type=pseudo_inv_type
    )

    # return the results
    return _kriging(
        variogram=variogram,
        grid_resolution=grid_resolution,
        return_type=return_type,
        plot_kwargs=kwargs,
        **args
    )
