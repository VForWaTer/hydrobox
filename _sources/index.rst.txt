.. HydroBox documentation master file, created by
   sphinx-quickstart on Tue May  4 09:33:00 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to HydroBox
===================

.. note::
   Major parts of the toolbox are currently re-written. Most interfaces of
   any function of version < 0.2 will most likely not work anymore.
   The aim is to produce a unified interface for hydrobox.
   Secondly, hydrobox is mainly pushed to reuse other Python packages within
   this scope, instead of re-implementing functions that are already there.

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Contents:

   toolboxes/index
   auto_examples/index

Installation
============

PyPI
----

Install hydrobox from the Python Pachage Index like:

.. code-block:: bash

   pip install hydrobox

Github
------

You can install hydrobox from source like:

.. code-block:: bash

   git clone git@github.com:vforwater/hydrobox
   cd hydrobox
   pip install -e .