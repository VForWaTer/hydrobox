.. HydroBox documentation master file, created by
   sphinx-quickstart on Thu Apr 19 08:08:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _ipython_directive:

Welcome to HydroBox's documentation!
====================================

.. image:: https://travis-ci.org/mmaelicke/hydrobox.svg?branch=master
    :target: https://travis-ci.org/mmaelicke/hydrobox

.. image:: https://readthedocs.org/projects/hydrobox/badge/?version=latest
    :target: http://hydrobox.readthedocs.io/en/latest?badge=latest

.. image:: https://codecov.io/gh/mmaelicke/hydrobox/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mmaelicke/hydrobox

.. warning::

    This documentation is by no means finished and in development. Kind of everything here might
    be subject to change.

About
=====


The HydroBox package is a toolbox for hydrological data analysis developed at the
`Chair of Hydrology`_ at the `Karlsruhe Institute of Technology (KIT)`_.
The HydroBox has a submodule called toolbox, which is a collection of functions and classes that accept common
numpy and pandas input formats and wrap around scipy functionality. This way can:

- speed up common hydrological data analysis tasks
- integrate fully with custom numpy/pandas/scipy code

Jump directly to the :doc:`installation section <installation>` or :doc:`get started <getting_started>`.

.. _Chair of Hydrology: https://hyd.iwg.kit.edu/english/index.php
.. _Karlsruhe Institute of Technology (KIT): https://kit.edu/english/index.php


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    installation
    getting_started
    examples/examples
    contribution
    reference/reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
