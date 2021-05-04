"""
Estimate a Variogram
====================

Use the geostatistics toolbox to estimate a variogram and use one of the many
plots.

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
# Estimate a variogram using a _exponential_ model and 25 distance lags
# that are derived from a KMeans cluster algorithm
# Here, we use the _describe_ output option to get a dictionary of 
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
# Create a plot of the variogram
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