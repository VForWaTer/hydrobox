"""
Geostatistical Toolbox
----------------------

This toolbox collects all functions needed to run different geostatistical
tasks. Variogram analysis can be done with :func:`variogram <hydrobox.geostat.variogram>`,
which wraps the scikit-gstat Variogram class.

Variogram estimation
~~~~~~~~~~~~~~~~~~~~

There are two major functions to estimate variograms. The :func:`variogram <hydrobox.geostat.variogram>`
function and the :func:`gridsearch <hydrobox.geostat.gridsearch>`, which will select optimal
variogram parameters, based on a cross-validated score.

.. minigallery::  hydrobox.geostat.variogram hydrobox.geostat.gridsearch
    :add-heading: Variogram examples

Content of :py:mod:`hydrobox.geostat`:

.. autosummary:: 
    :toctree: gen_modules/
    :template: module.rst

    variogram
    gridsearch

Kriging
~~~~~~~

Kriging can be performed, after a variogram was estimated. the :class:`Variogram <skgstat.Variogram>`
is exported to gstools and one of the :class:`Krige <gstools.Krige>` classes will be used for
kriging.

.. minigallery:: hydrobox.geostat.simple_kriging hydrobox.geostat.ordinary_kriging hydrobox.geostat.universal_kriging hydrobox.geostat.ext_drift_kriging
    :add-heading: Kriging examples

.. autosummary::
    :toctree: gen_modules/
    :template: module.rst

    simple_kriging
    ordinary_kriging
    universal_kriging
    ext_drift_kriging

"""
from .variogram import variogram
from .gridsearch import gridsearch
from .kriging import ordinary_kriging, simple_kriging, universal_kriging, ext_drift_kriging