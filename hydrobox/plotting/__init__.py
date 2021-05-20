"""
Plotting routines
-----------------

Some of the tools, which have results plot may call a 
common interface of the `hydrobox.plotting` submodule. 
These interfacing functions in turn will either call 
a matplotlib, bokeh or plotly implementation.

This is primarily implemented for convenience. The 
usecase in V-FOR-WaTer, the context at which this 
library is developed is to have a pythonic tool able to 
handle matplotlib plots, but also get interactive HTML 
versions of such by using bokeh or plotly. 

.. warning::

    This feature is experimental and may be completely or 
    partly deprecated. Either bokeh or plotly may be removed 
    on any version < 1.0.0 in favor of the other.

"""
from ._backend import plotting_backend, plot_function_loader
