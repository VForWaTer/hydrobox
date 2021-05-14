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
        dims = [range(grid_resolution) for _ in range(variogram.dim)]
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
    grid_resolution: int = None,
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