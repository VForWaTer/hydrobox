from typing import Dict, List, Tuple, Any, Literal
import skgstat as skg
from sklearn.model_selection import GridSearchCV
import numpy as np


def gridsearch(
    param_grid: Dict[str, Tuple],
    variogram: skg.Variogram = None,
    coordinates: np.ndarray = None,
    values: np.ndarray = None,
    score: Literal['rmse', 'mse', 'mae'] = 'rmse',
    cross_validate: bool = True,
    n_jobs=-1,
    return_type: Literal['object', 'best_param'] = 'object',
    **kwargs
) -> Dict[str, Any]:
    """
    Automated GridSerarch for best variogram parameters.
    Uses :class:`GridSearchCV <sklearn.model_selection.GridSearchCV>` to
    find the best parameter set.

    .. todo::
        with scikit-gstat 0.6, remove the cross_validate check.

    Parameters
    ----------
    param_grid : dict
        List of parameters that should be used to form the grid.
        Each key has to be a valid argument to :class:`Variogram <skgstat.Variogram>`
        along with a list of valid options to try.
    variogram : skgstat.Variogram
        Variogram instance that should be used to find more suitable
        parameters. If given, coordinates, values and kwargs will be
        ignored
    coordinates : numpy.ndarray
        Array of coordinates. Mandatory if variogram is None.
    values : numpy.ndarray
        Array of values. Mandatory if variogram is None.
    score : str
        Score to find the best parameter set. Has to be one of
        ['rmse', 'mse', 'mae']
    cross_validate : bool
        If True (default) the score will be applied to a leave-one-out
        cross-validation of a Kriging using the current Variogram.
        If False, the model fit to the experimental variogra, will be scored.
        .. note:: 
            Needs at least `scikit-gstat>=0.5.4`.
    n_jobs : int
        Will be passed down to :class:`GridSearchCV <sklearn.model_selection.GridSearchCV>`
    return_type : str
        Either `'object'`, to return the GridSerachCV object or
        `'best_param'` to return a dictionary of the best params.


    Returns
    -------
    gridSearch : sklearn.model_selection.GridSearchCV
        if return type is `'object'`
    best_params : dict
        if return type is `'best_param'`

    Raises
    ------
    AttributeError : 
        if neither a :class:`Variogram <skgstat.Variogram>` or both
        coordinates and values are given
    
    See Also
    --------
    skgstat.interface.VariogramEstimator
    sklearn.model_selection.GridSearchCV

    """
    if variogram is None and (coordinates is None or values is None):
        raise AttributeError('Either a Variogram or the coorinates, values and kwargs needs to be set')
    
    # extract the parameters
    if variogram is not None:
        coordinates = variogram.coordinates
        values = variogram.values
        kwargs.update(variogram.describe().get('params'))

    # handle cross-validate
    _, skg_m, skg_p = skg.__version__.split('.')
    if int(skg_m) > 5 or int(skg_p) >= 4:  # pragma: no cover
        kwargs['cross_validate'] = cross_validate

    # initialize the estimator
    estimator = skg.interfaces.VariogramEstimator(
        use_score=score,
        **kwargs
    )

    # inistialize the GridSearch
    gs = GridSearchCV(estimator, param_grid, cv=5, n_jobs=n_jobs)

    # run
    gs_fit = gs.fit(coordinates, values)

    if return_type.lower() == 'object':
        return gs_fit
    elif return_type.lower() == 'best_param':
        return gs_fit.best_params_

