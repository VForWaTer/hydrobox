"""
GridSearch optimization
=======================

The SciKit-GStat package can be connected to scikit-learn i.e. to use
the model optimization sub-package. In this example, different options
are compared and cross-validated.
The Interface has two different options to evaluate a variogram model fit:

* goodness of fit measures of the spatial model itself
* cross-validation of the variogram by interpolating the observation points

Both options can use the RMSE, MSE and MAE as a metric.

"""
import plotly
import plotly.graph_objects as go
import hydrobox
from hydrobox.data import pancake
from hydrobox.plotting import plotting_backend
plotting_backend('plotly')

#%%
# Load sample data from the data sub-module

df = pancake()

#%%
# First, a Variogram is estimated, which will fix all arguments that
# should not be evaluated by the Grid Search.

vario = hydrobox.geostat.variogram(
    coordinates=df[['x', 'y']].values,
    values=df.z.values,
    maxlag=500,
    bin_func='kmeans',
    return_type='object'
)

#%% 
# The next step is to create a parameter grid, which specifies the
# value space for each parameter that should be checked.
# Here, we will try all combinations of different models and lag classes.

param_grid = {
    'model': ('spherical', 'exponential', 'matern'),
    'n_lags': (15, 20, 25, 30, 35)
}

#%%
# First the model fit itself is evaluated and only the best parameter
# set will be returned

best_param = hydrobox.geostat.gridsearch(
    param_grid=param_grid,
    variogram=vario,
    coordinates=None,       # must be set if variogram is None
    values=None,            # must be set if variogram is None
    score='rmse',           # default
    cross_validate=False,   # evaluate model fit,
    n_jobs=-1,              # use parallel mode
    return_type='best_param'
)

print(best_param)

#%%
# It is also possible to return the underlying 
# :class:`GridSearchCV <sklearn.model_selection.GridSearchCV>` instance.
# This class holds way more information than just the best parameter.

# reun the same Gridsearch, return the object
clf = hydrobox.geostat.gridsearch(
    param_grid=param_grid,
    variogram=vario,
    coordinates=None,       # must be set if variogram is None
    values=None,            # must be set if variogram is None
    score='rmse',           # default
    cross_validate=False,   # evaluate model fit,
    n_jobs=-1,              # use parallel mode
    return_type='object'
)

# get the scores and their std
scores = clf.cv_results_['mean_test_score']
scores_std = clf.cv_results_['std_test_score']
x = range(len(scores))

#%%
# Plot the result
fig = go.Figure()
fig.add_trace(
    go.Scatter(x=x, y=scores, mode='lines', line_color='#A3ACF7')
)
fig.add_trace(
    go.Scatter(x=x, y=scores + scores_std, mode='lines', line_color='#BAC1F2', fill='tonexty')
)
fig.add_trace(
    go.Scatter(x=x, y=scores - scores_std, mode='lines', line_color='#BAC1F2', fill='tonexty')
)
fig.update_layout(
    template='plotly_white'
)

# show the plot
plotly.io.show(fig)