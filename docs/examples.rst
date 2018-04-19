========
Examples
========

.. toctree::
    :maxdepth: 2


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
        size=None                    # set to None, for infering
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
the last five values. The output as `numpy.ndarray` is especially useful when the output shall be
directed into another analysis function or is used inside a workflow engine. This way the
plotting and styling can be adepted to the use-case.

However, in case you are using the tools in a pure Python environment, most tools can be directly
 used for plotting. At the current stage, `matplotlib` is the only plotting possibility.

Plot the result
---------------

.. ipython:: python

    # If not encapsulated in a WPS server, the tool can also plot
    @savefig examples_single_fdc.png width=5in
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
    @savefig examples_double_fdc.png width=10in
    plt.show();
