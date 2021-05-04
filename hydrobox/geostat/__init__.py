"""
Geostatistical Toolbox
----------------------

This toolbox collects all functions needed to run different geostatistical
tasks. Variogram analysis can be done with :func:`variogram <hydrobox.geostat.variogram>`,
which wraps the scikit-gstat Variogram class.

.. minigallery:: hydrobox.geostat.variogram hydrobox.geostat.gridsearch
    :add-heading: Geostatistics examples

Content of :py:mod:`hydrobox.geostat`:

.. autosummary:: 
    :toctree: gen_modules/
    :template: module.rst

    variogram
    gridsearch

"""
from .variogram import variogram
from .gridsearch import gridsearch