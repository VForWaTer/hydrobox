# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'HydroBox'
copyright = '2021, Mirko Mälicke'
author = 'Mirko Mälicke'

# The full version, including alpha/beta/rc tags
release = '0.2.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.todo'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# intesphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None),
    'skgstat': ('https://mmaelicke.github.io/scikit-gstat', None),
    'gstools': ('https://geostat-framework.readthedocs.io/projects/gstools/en/latest', None)
}

from plotly.io._sg_scraper import plotly_sg_scraper
image_scrapers = ('matplotlib', plotly_sg_scraper,)

import sphinx_gallery

# Sphinx Gallery config
sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'gallery_dirs': 'auto_examples',
    'backreferences_dir': 'gen_modules/backreferences',
    'doc_module': ('hydrobox',),
    'image_scrapers': image_scrapers,
}

autosummary_generate = True
