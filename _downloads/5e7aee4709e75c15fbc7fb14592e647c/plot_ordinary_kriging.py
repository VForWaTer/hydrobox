"""
Ordinary Kriging
================

With the help of a variogram that describes spatial properties of 
a sample, the sample can be interpolated. 

"""
from time import time
import plotly
import hydrobox
from hydrobox.data import pancake
from hydrobox.plotting import plotting_backend
plotting_backend('plotly')

#%%
# Load sample data from the data sub-module

df = pancake()

#%%
# Estimate a exponential variogram again. More details are given in the 
# :ref:`plot_variogram.py` example.

vario = hydrobox.geostat.variogram(
    coordinates=df[['x', 'y']].values,
    values=df.z.values,
    model='exponential',
    bin_func='kmeans',
    n_lags=25,
    return_type='object'
)

#%%
# Run ordinary kriging on a 100x100 grid. In this run, the result is 
# directly plotted. Other return types are ``'grid'``, to return the 
# resulting interpolated grid and kriging error grid, or ``'object'``
# to return the :class:`Krige <gstools.Krige>` class. This class 
# is already parameterized, but the interpolation was not yet performed.
# This is most helpful if other grid should be constructed.

t1 = time()
fig = hydrobox.geostat.ordinary_kriging(
    variogram=vario,
    grid_resolution=100,
    exact=True,
    cond_err='nugget',
    return_type='plot'
)
t2 = time()

print('Took: %2f sec' % (t2 - t1))

# show the plot
plotly.io.show(fig)