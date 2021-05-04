from hydrobox import data
import hydrobox
import plotly.graph_objects as go
import skgstat as skg
from sklearn.model_selection import GridSearchCV


def test_variogram():
    """Test the return types"""
    # get data
    df = data.pancake()
    hydrobox.plotting_backend('plotly')

    for t, type_ in zip(('object', 'describe', 'plot'), (skg.Variogram, dict, go.Figure)):
        vario = hydrobox.geostat.variogram(
            df[['x', 'y']].values,
            df.z.values,
            return_type=t
        )

        assert isinstance(vario, type_)


def test_gridsearch():
    """Test Gridsearch with explicit param_grid"""
    # create the grid
    param_grid={'model': ('spherical', 'gaussian', 'stable')}

    # get data
    df = data.pancake()
    
    gs = hydrobox.geostat.gridsearch(
        param_grid=param_grid,
        coordinates=df[['x', 'y']].values,
        values=df.z.values,
        n_lags=25,
        return_type='object'
    )

    assert isinstance(gs, GridSearchCV)

def test_gridsearch_variogram():
    """Test Gridsearch with variogram passed"""
    df = data.pancake()
    # create the grid
    param_grid={'fit_method': ('trf', 'lm', 'ml')}
    vario = hydrobox.geostat.variogram(
            df[['x', 'y']].values,
            df.z.values,
            n_lags=15,
            return_type='object'
        )
    gs = hydrobox.geostat.gridsearch(
        param_grid,
        variogram=vario,
        return_type='best_param'
    )

    assert isinstance(gs, dict)