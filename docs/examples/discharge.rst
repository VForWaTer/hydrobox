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

The workflow in this example will generate some random data and applies two
processing  steps to illustrate the general idea. All tools are designed to fit
seamlessly  into automated processing environments like WPS servers or other workflow engines.


The workflow in this example:

  #. generates a ten year random discharge time series from a gamma distribution
  #. aggregates the data to daily maximum values
  #. creates a flow duration curve
  #. uses python to visualize the flow duration curve

Generate the data
-----------------

.. ipython:: python

    # use the ggplot plotting style
    import matplotlib as mpl
    mpl.style.use('ggplot')
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


Calculate the flow duration curve (FDC)
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
useful when the output is directed into another analysis function or is used inside a workflow engine. This way the
plotting and styling can be adapted to the use-case.

However, in case you are using hydrobox in a pure Python environment, most tools can be directly
 used for plotting. At the current stage ``matplotlib`` is the only plotting
 possibility.

Plot the result
---------------

.. ipython:: python

    # If not encapsulated in a WPS server, the tool can also plot
    @savefig examples_single_fdc.png width=4in
    toolbox.flow_duration_curve(series_daily.values);


With most plotting functions, it is also possible to embed the plots into existing figures in
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

In this example, we will use real world data. As the hydrobox is build on top
of numpy and pandas, we can easily use the great input tools provided by
pandas. This example will load a discharge time series from Hofkirchen in
Germany, gauging the Danube river. The data is provided by
`Gewässerkundlicher Dienst Bayern`_ under a CC BY 4.0 license.
Therefore, this example will also illustrate how you can combine pandas and
hydrobox to produce nice regime plots with just a few lines of code.

.. _Gewässerkundlicher Dienst Bayern: https://gkd.bayern.de

.. note::

    In order to make use of the plotting, you need to run the tools in a
    Python environment. If you are using e.g. a WPS server calling the
    tools, be sure to capture the output.

Load the data using pandas
--------------------------

.. ipython:: python

    # some imports
    from hydrobox import toolbox
    import pandas as pd
    # Step 1:
    df = pd.read_csv('./data/discharge_hofkirchen.csv',
        skiprows=10,            # meta data header, skip this
        sep=';',                # the cell separator
        decimal=',',             # german-style decimal sign
        index_col='Datum',      # the 'date' column
        parse_dates=[0]         # transform to DatetimeIndex
    )
    # use only the 'Mittelwert' (mean) column
    series = df.Mittelwert
    print(series.head())

.. note::

    The data was downloaded from: `Datendownload GKD`_ and is published under
    CC BY 4.0 license. If you are not using a german OS, note that the file
    encoding is ISO 8859-1 and you might have to remove the special german
    signs from the header before converting to UTF-8.


.. _Datendownload GKD: https://gkd.bayern.de/fluesse/download/index.php?thema=gkd&rubrik=fluesse&produkt=abfluss&gknr=0&msnr=10088003

.. seealso::

    More information on the :func:`read_csv function <pandas:pandas.read_csv>`
     is provided in the `pandas documentation`_.


.. _pandas documentation: https://pandas.pydata.org/pandas-docs/stable

Output the regime
-----------------

In order to calculate the regime, without a plot, we can set ``plot`` to `None`.

.. ipython:: python

    regime = toolbox.regime(series, plot=False)
    print(regime)

These plain numpy arrays can be used in any further custom workflow or plotting.

Plotting
--------

.. ipython:: python

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

Using percentiles
-----------------

The plot shown above is nice, but the tool is way more powerful. Using the
``percentiles`` keyword, we can either specify a number of percentiles or
pass custom percentile edges.

.. ipython:: python

    @savefig examples_regime_percentile.png width=6in
    toolbox.regime(series, percentiles=10);

.. ipython:: python

    @savefig examples_regime_percentile2.png width=6in
    toolbox.regime(series, percentiles=[25, 75, 100], color='#223a5e');

Adjusting the plot
------------------

Furthermore, the regime function can normalize the monthly aggregates to the
overall aggregate. The function used for aggregation can also be changed. The
following example will output monthly mean values over median values and
normalize them to the MQ (overall mean).

.. ipython:: python

    @savefig examples_regime_normalize.png width=6in
    toolbox.regime(series, agg='nanmean', normalize=True, color='#223a5e')

Reference
---------

.. seealso::

    - :ref:`regime reference <reference_regime>`
