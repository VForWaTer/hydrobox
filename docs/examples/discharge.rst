===============
Discharge Tools
===============

.. toctree::
    :maxdepth: 2


.. _example_fdc:

FDC from random data
====================

Workflow
--------

The workflow to be presented in this example will generate some random data and apply two
processing  steps. This shall illustrate the general idea. All tools are designed to fit
seamlessly  into automated processing environments like a WPS server or other workflow engines.


The workflow to be presented:

  #. generate a ten year random discharge time series from a gamma distribution
  #. aggregate the data to daily maximum values
  #. create a flow duration curve
  #. use python to visualize the flow duration curve

Generate the data
-----------------

.. ipython:: python

    from hydrobox import toolbox
    # Step 1:
    series = toolbox.io.timeseries_from_distribution(
        distribution='gamma',
        distribution_args=[2, 0.5],  # [location, scale]
        start='200001010000',        # start date
        end='201001010000',          # end date
        freq='15min',                # temporal resolution
        size=None,                   # set to None, for inferring
        seed=42                      # set a random seed
    )
    print(series.head())


Apply the aggregation
---------------------

.. ipython:: python

    import numpy as np
    series_daily = toolbox.aggregate(series, by='1D', func=np.max)
    print(series_daily.head())


Calaculate the FDC
------------------

.. ipython:: python

    # the FDC is calculated on the values only
    fdc = toolbox.flow_duration_curve(x=series_daily.values,     # an FDC does not need a DatetimeIndex
                                  plot=False                 # return values, not a plot
                                 )
    print(fdc[:5])
    print(fdc[-5:])


The first output line shows the first five exceeding probabilities, while the second line shows
the last five values. The output as :py:class:`numpy.ndarray` is especially
useful when the output shall be
directed into another analysis function or is used inside a workflow engine. This way the
plotting and styling can be adepted to the use-case.

However, in case you are using the tools in a pure Python environment, most tools can be directly
 used for plotting. At the current stage, ``matplotlib`` is the only plotting
 possibility.

Plot the result
---------------

.. ipython:: python

    # If not encapsulated in a WPS server, the tool can also plot
    @savefig examples_single_fdc.png width=4in
    toolbox.flow_duration_curve(series_daily.values);


With most plotting functions, it is also possbile to embed the plots into existing figures in
order to fit seamlessly into reports etc.

.. ipython:: python

    import matplotlib.pyplot as plt
    # build the figure as needed
    fig, axes = plt.subplots(1,2, figsize=(14,7))
    toolbox.flow_duration_curve(series_daily.values, ax=axes[0]);
    toolbox.flow_duration_curve(series.values, ax=axes[1]);
    axes[0].set_title('aggregated');
    axes[1].set_title('non-aggregated');
    @savefig examples_double_fdc.png width=8in
    plt.show();

Reference
---------

.. seealso::

    - :ref:`flow_duration_curve reference <reference_flow_duration_curve>`
    - :ref:`aggregate reference <reference_aggregate>`



.. _example_regime:

Hydrological Regime
===================

Workflow
--------

The workflow for the :ref:`regime function <reference_regime>` is very
similar to the one presented in the :ref:`flow duration curve <example_fdc>`
section.

A random discharge time series will be generated and directly passed to the
regime function. Additionally, different ways of adjusting the plot output
will be presented.

.. note::

    In order to make use of the plotting, you need to run the tools in a
    Python environment. If you are using e.g. a WPS server calling the
    tools, be sure to capture the output.

Generate the data
-----------------

.. ipython:: python

    from hydrobox import toolbox
    # Step 1:
    series = toolbox.io.timeseries_from_distribution(
        distribution='gamma',
        distribution_args=[2, 0.5],  # [location, scale]
        start='200001010000',        # start date
        end='201001010000',          # end date
        freq='15min',                # temporal resolution
        size=None,                   # set to None, for inferring
        seed=42                      # Set a random seed
    )
    print(series.head())

Output the regime
-----------------

In order to calculate the regime, without a plot, we can set ``plot`` to `None`.

.. ipython:: python

    regime = toolbox.regime(series, plot=False)
    print(regime)

These plain numpy array can be used in any further custom workflow or plotting.

Plotting
--------

.. ipython:: python

    # use the ggplot plotting style
    import matplotlib as mpl
    mpl.style.use('ggplot')
    @savefig examples_regime.png width=6in
    toolbox.regime(series)

.. note::

    As stated in the :ref:`function reference <reference_regime>`, the default
    plotting will choose the first color of the specified color map for the main
    aggregate line. As this defaults to the ``Blue``s, the first color is white.
    Therefore, when no percentiles are used (which would make use of the
    colormap), it is a good idea to overwrite the color for the main line.

.. ipython:: python

    @savefig examples_regime2.png width=6in
    toolbox.regime(series, color='#ffab7f')

Reference
---------

.. seealso::

    - :ref:`regime reference <reference_regime>`
