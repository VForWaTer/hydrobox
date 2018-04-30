=================
Signal Processing
=================

.. toctree::
    :maxdepth: 2


Simplifying a Signal
====================

Whenever you seek to apply a tool on your data that will operate on each
value and this tool is time and / or resource consuming, it might be a good
idea to operate on as little values as possible. Simply removing duplicated
values from a signal is not always working. Think of a discharge time series
where you want to calculate a index that is depending on a previous state.

Set up a test case
------------------

The example below will show the idea behind the
:ref:`simplify<reference_simplify>` method of the ``singal`` submodule. At
forst some imports.

.. ipython:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.style.use('ggplot')

And now setup and plot the test signal.

.. ipython:: python

    x = np.array([1., 1.2, 1.5, 1.5, 1.5, 1.5, 1.6, 1.5, 1.6, 1.5, 1., 0.5,
                  0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3,
                  0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.7, 1., 1.5, 1.6,
                  1.5, 1.6, 1.5, 1.6, 1.5, 1.6])
    @savefig examples_sample_data.png width=6in
    plt.plot(x, '.--r');

Handling replicas
-----------------

There are a number of replications, that we want to get rid of.

.. ipython:: python

    from hydrobox.toolbox import simplify
    @savefig examples_simplified_sample.png width=6in
    plt.plot(simplify(x, flatten=False), '.--r');

Look at the amount of markers in both plots, where the signal gave a constant
 value. The replicas got dropped off from the signal.

Handling sensor precision noise
-------------------------------

So far, that did only remove subsequent duplicates in value. The other signal
information this method can simplify is the constant repetition of two values.
This usually happens in environmental sensors either at constant conditions
or at really slow state changes. Then the signal can alternate between two
states at its sensor precision. These recordings can be evened out by setting
the ``flatten`` attribute to True.

.. ipython:: python

    @savefig examples_simplified_sample2.png width=6in
    plt.plot(simplify(x, flatten=True), '.--r');

Of course, the index information got completely lost. In this example the
x-axis is just counting the occurrences of values. In case you need the index
information for further analysis, you have to extract the index and preserve
it, before calling the simplify method.

.. important::

    The preservation of indices, whenever the data is of type ``pandas.Series``
    is planned for a future release.


.. warning::

    Keep in mind that two very strong assumptions are underlying this method.
    It does change the signal dramatically. Ensuring that the sensor noise
    assumption is correct, is completely up to you.