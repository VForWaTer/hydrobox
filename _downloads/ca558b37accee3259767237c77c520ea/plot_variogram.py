"""
Estimate a Variogram
====================

Use the geostatistics toolbox to estimate a variogram and use one of the many
plots. These plots help to understand the spatial properties of a variogram,
and finally, the :class:`Variogram <skgstat.Variogram>` object itself can be
returned and used in one of the Kriging routines.

"""
from pprint import pprint
import plotly
import hydrobox
from hydrobox.data import pancake
from hydrobox.plotting import plotting_backend
plotting_backend('plotly')

# %%
# Load sample data from the data sub-module

df = pancake()

# %%
# Estimate a variogram using a exponential model and 25 distance lags
# that are derived from a KMeans cluster algorithm
# Here, we use the describe output option to get a dictionary of 
# all variogram parameters

vario = hydrobox.geostat.variogram(
    coordinates=df[['x', 'y']].values,
    values=df.z.values,
    model='exponential',
    bin_func='kmeans',
    n_lags=25,
    return_type='describe'
)
# print
pprint(vario)

#%% 
# There are various return types, one of them is the plot.
# This is the main plotting tool for variogram instances
fig = hydrobox.geostat.variogram(
    coordinates=df[['x', 'y']].values,
    values=df.z.values,
    model='exponential',
    bin_func='kmeans',
    n_lags=25,
    return_type='plot'
)

# show the figure
plotly.io.show(fig)

#%%
# Alternatively you can return the :class:`Variogram <skgstat.Variogram>`
# object itself and use all the different settings and methods directly.

v = hydrobox.geostat.variogram(
    coordinates=df[['x', 'y']].values,
    values=df.z.values,
    model='exponential',
    bin_func='kmeans',
    n_lags=25,
    return_type='object'
)

pprint(v)

#%% 
# The :class:`Variogram <skgstat.Variogram>` has a plotting method for
# all point pairs at their separating distances. It is available as a 
# return type, but can also be called directly:
fig = v.distance_difference_plot() 

plotly.io.show(fig)

#%%
# The variogram instance has a lot of quality measures to judge the goodness
# of fit for the theoretical model. They are implemented as properties and can
# be used like attribtues, while being always up to date if the variogram is mutated.
# Another helpful method is :func:`cross_validate <skgstat.Variogram.cross_validate>`.
# This will run a leave-one-out cross validation by interpolating the missing point for 
# all points. This is especially useful in cases, where a theoretical model fits well,
# but the spatial properties are not well captured. 

# calculate the rmse of the model
print(f"{v.model.__name__} RMSE:  {v.rmse}")

# get the cross-validation time
from time import time
t1 = time()
rmse = v.cross_validate()
t2 = time()
print('Cross-validated RMSE: %.2f  (took: %2fs)' % (rmse, t2 - t1))
