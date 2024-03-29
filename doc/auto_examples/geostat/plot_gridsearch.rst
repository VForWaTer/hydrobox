
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "auto_examples/geostat/plot_gridsearch.py"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_geostat_plot_gridsearch.py>`
        to download the full example code

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_geostat_plot_gridsearch.py:


GridSearch optimization
=======================

The SciKit-GStat package can be connected to scikit-learn i.e. to use
the model optimization sub-package. In this example, different options
are compared and cross-validated.
The Interface has two different options to evaluate a variogram model fit:

* goodness of fit measures of the spatial model itself
* cross-validation of the variogram by interpolating the observation points

Both options can use the RMSE, MSE and MAE as a metric.

.. GENERATED FROM PYTHON SOURCE LINES 16-23

.. code-block:: default

    import plotly
    import plotly.graph_objects as go
    import hydrobox
    from hydrobox.data import pancake
    from hydrobox.plotting import plotting_backend
    plotting_backend('plotly')








.. GENERATED FROM PYTHON SOURCE LINES 24-25

Load sample data from the data sub-module

.. GENERATED FROM PYTHON SOURCE LINES 25-28

.. code-block:: default


    df = pancake()








.. GENERATED FROM PYTHON SOURCE LINES 29-31

First, a Variogram is estimated, which will fix all arguments that
should not be evaluated by the Grid Search.

.. GENERATED FROM PYTHON SOURCE LINES 31-40

.. code-block:: default


    vario = hydrobox.geostat.variogram(
        coordinates=df[['x', 'y']].values,
        values=df.z.values,
        maxlag=500,
        bin_func='kmeans',
        return_type='object'
    )








.. GENERATED FROM PYTHON SOURCE LINES 41-44

The next step is to create a parameter grid, which specifies the
value space for each parameter that should be checked.
Here, we will try all combinations of different models and lag classes.

.. GENERATED FROM PYTHON SOURCE LINES 44-50

.. code-block:: default


    param_grid = {
        'model': ('spherical', 'exponential', 'matern'),
        'n_lags': (15, 20, 25, 30, 35)
    }








.. GENERATED FROM PYTHON SOURCE LINES 51-53

First the model fit itself is evaluated and only the best parameter
set will be returned

.. GENERATED FROM PYTHON SOURCE LINES 53-67

.. code-block:: default


    best_param = hydrobox.geostat.gridsearch(
        param_grid=param_grid,
        variogram=vario,
        coordinates=None,       # must be set if variogram is None
        values=None,            # must be set if variogram is None
        score='rmse',           # default
        cross_validate=False,   # evaluate model fit,
        n_jobs=-1,              # use parallel mode
        return_type='best_param'
    )

    print(best_param)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    {'model': 'spherical', 'n_lags': 35}




.. GENERATED FROM PYTHON SOURCE LINES 68-71

It is also possible to return the underlying 
:class:`GridSearchCV <sklearn.model_selection.GridSearchCV>` instance.
This class holds way more information than just the best parameter.

.. GENERATED FROM PYTHON SOURCE LINES 71-89

.. code-block:: default


    # reun the same Gridsearch, return the object
    clf = hydrobox.geostat.gridsearch(
        param_grid=param_grid,
        variogram=vario,
        coordinates=None,       # must be set if variogram is None
        values=None,            # must be set if variogram is None
        score='rmse',           # default
        cross_validate=False,   # evaluate model fit,
        n_jobs=-1,              # use parallel mode
        return_type='object'
    )

    # get the scores and their std
    scores = clf.cv_results_['mean_test_score']
    scores_std = clf.cv_results_['std_test_score']
    x = list(range(len(scores)))








.. GENERATED FROM PYTHON SOURCE LINES 90-91

Plot the result

.. GENERATED FROM PYTHON SOURCE LINES 91-106

.. code-block:: default

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=scores, mode='lines', line_color='#A3ACF7', name='RMSE score')
    )
    fig.add_trace(
        go.Scatter(x=x, y=scores + scores_std, mode='lines', line_color='#BAC1F2', fill='tonexty', name='RMSE + std')
    )
    fig.add_trace(
        go.Scatter(x=x, y=scores - scores_std, mode='lines', line_color='#BAC1F2', fill='tonexty', name='RMSE - std')
    )
    fig.update_layout(
        template='plotly_white'
    )

    # show the plot
    plotly.io.show(fig)


.. raw:: html
    :file: images/sphx_glr_plot_gridsearch_001.html






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 1 minutes  23.717 seconds)


.. _sphx_glr_download_auto_examples_geostat_plot_gridsearch.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_gridsearch.py <plot_gridsearch.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_gridsearch.ipynb <plot_gridsearch.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
