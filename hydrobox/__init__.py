import sys

# Python 3.3 is not supported.
if sys.version_info < (3, 8):
    raise ImportError('Python < 3.8 is not supported')


import hydrobox.utils
from hydrobox.plotting._backend import plotting_backend

__version__ = '0.1.6'
__plot_backend__ = 'matplotlib'
