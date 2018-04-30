==================
Contribution Guide
==================

.. toctree::
    :maxdepth: 2

.. role:: pycode(code)
    :language: python

How to Contribute
=================

There are several ways, how you can contribute to hydrobox. All contributions
shall make use of the Fork / Pull request workflow in the `GitHub repository`_.
More information on pull requests can be found on the `GitHub About pull requests`_
page.

    #. Add new tools to the toolbox
    #. Improve / Add unittest to increase code coverage
    #. Improve / Add docstrings on existing functions
    #. Add more examples to the documentation

.. _GitHUb repository: https://github.com/mmaelicke/hydrobox.git
.. _GitHub About pull requests: https://help.github.com/articles/about-pull-requests


Add Tools to the Toolbox
------------------------

.. important::

    In a nutshell:
        #. Fork the repository on GitHub
        #. Commit your method to your fork
        #. Add documentation and unittests for your method
        #. Make sure your fork is building correctly
        #. Pull request your fork back into the main repository

The idea behind hydrobox is to be used on top of numpy, scipy and pandas.
This implies usage the data types defined in these libraries whenever possible.
The main purpose of hydrobox is to save hydrologists from reproducing their
codes in every single project. Therefore a hydrobox tool shall:

    #. combine analysis steps belonging together into one function, while
    #. separating preprocessing from analysis
    #. be helpful for other hydrologists
    #. output common python, numpy or pandas datatypes


.. important::

    For this guide, we will add a function ``from_csv`` to the ``io``
    submodule. This should illustrate how you can add your stuff.

Fork and structure
~~~~~~~~~~~~~~~~~~

Once you forked the project, place a new file in the appropriate module or
add a new one. Once your function has been added, import your function in the
``hydrobox.toolbox`` file Please use an expressive name for your function. It
should be clear what the
function does. . In some cases tool functions are tool specific to
make them available at the global ``hydrobox.toolbox`` scope. Then the
submodule itself will be imported in the toolbox and you do not need to
adjust the imports. One example is the ``io`` submodule.

Here, we pretend to add a ``from_csv`` file to the toolbox. This function
will go into a file ``text.py`` in the ``hydrobox.io`` submodule:

.. code-block:: python
    :linenos:

    def from_csv(path, sep=','):
        """
        numpydoc docstring here
        """
        return pd.from_csv(path, sep=sep)


Now, import this function in the ``__init__`` of ``hydrobox.io``. If your
method shall be available in the global scope, import it in
``hydrobox.toolbox``, as well.

.. important::

    Please do only use `numpydoc`_ docstring conventions and make sure to
    properly style and comment the Parameters section.

.. _numpydoc: http://numpydoc.readthedocs.io/en/latest/format.html


Decorating your tool
~~~~~~~~~~~~~~~~~~~~

Hydrobox includes two helpful decorators in the ``hydrobox.util`` submodule:
:pycode:`accept` and :pycode:`enforce`. We encourage you to use the
:pycode:`accept` decorator whenever possible. This will help to produce way
cleaner code.
This decorator will check the input data for their data type and raise a
:pycode:`TypeError` in case the passed data does not have the correct type.
If more than one type is accepted, simply pass a tuple. In case a argument can
be on :pycode:`NoneType` or a :pycode:`callable`, use the two literals
:pycode:`'None'` and :pycode:`'callable'` and pass them as strings.

.. code-block:: python
    :linenos:

    from io import TextIOWrapper
    @accept(path=(str, TextIOWrapper), sep=str)
    def from_csv(path, sep=','):
        ...

In this example, the :pycode:`path` argument can be a string or a file pointer,
:pycode:`sep` has to be a string. Thus, there is no need to check the user
input in your tool, as the decorator already did this for you.
We encourage you to use this decorator especially for checking the input data
to be of type :class:`numpy:numpy.ndarray` :class:`pandas:pandas.DataFrame`
and :class:`pandas:pandas.Series`.


Test your tool
~~~~~~~~~~~~~~

Although the code coverage of this project is not yet really good, it would be nice not to drop
it any further. A good code coverage needs unit tests. Beyond code coverage, unit tests will help
us to detect whenever our contribution breaks existing code. And last but not least a unit test
will help yourself to build more reliable code.
In a nutshell, it would be really helpful if you produce unit tests for your code. More
information on unit tests is given in the :ref:`Add / Improve unittests <contrib_unittests>`
section. Some useful links to get you stated with unittests in Python can be found below.

.. seealso::

    - `unittests module reference`_
    - `Unit Test Wikipedia page`_
    - :ref:`Add / Improve unittests <contrib_unittests>`

.. _unittests module reference: https://docs.python.org/3/library/unittest.html
.. _Unit Test Wikipedia page: https://en.wikipedia.org/wiki/Unit_testing



Document your tool
~~~~~~~~~~~~~~~~~~

In order to make it possible for others to use your tool, a good, comprehensive documentation is
needed. As a first step, you sould always add a docstring to your function. For hydrobox, please
use the `numpydoc`_ docstring format. More information can also be found in the
:ref:`Add / Improve docstrings <contrib_docstrings>` section.

.. seealso::

    - `numpydoc reference site <numpydoc>`_
    -  :ref:`Add / Improve docstrings <contrib_docstrings>`

Produce examples
~~~~~~~~~~~~~~~~

Sometimes a docstring is not enough to understand a Tool. Although short examples, references and
 formulas can go into numpydoc docstring formats, you might want to offer different examples
 covering the whole bandwidth of your tool. Then you should produce some examples into this
 documentation. You can refer to the :ref:`Examples <contrib_examples>` section for more
 information.

.. seealso::

    - :ref:`Examples <contrib_examples>`

Pull Request
~~~~~~~~~~~~

Once your finished with your implementations, create a pull request on GitHub.
More info in the :ref:`Pull Request <contrib_pull>` section.

.. _contrib_unittests:

Add / improve unittests
=======================

.. important::

    If you are not familiar with unit testing in general, please refer to
    https://en.wikipedia.org/wiki/Unit_testing. If you are not familiar with
    the ``unittests`` module. please refer to
    https://docs.python.org/3/library/unittest.html

Unit tests are important as they make your code much more reliable and
reusable for other users. The basic idea behind a unit test is to test any
possible input and output to your tool against the expected behavior. For
this you have to set up a test case, run the scenario and compare it to what
you expected. In case some modules and packages you rely on change and break
your code, the unit test will notice this and fail. I am personally using
unit tests whenever I try to improve my code, this way I can be sure, that I
did not optimize any functionality away (and that happens a lot...).

For creating a unit test you need to define a class. Each method of this
class represents a test. There are different ways of implementing unit tests,
either one test method to test a whole tool or one test method per single
check you want to perform. In hydrobox, we decided to use one TestCase class
for each method and try to break down each check into a single test method.
The example below should illustrate this behavior.

.. code-block:: python
    :linenos:

    import unittest
    import pandas as pd
    import from_csv         # import your tool here

    class TestFromCsv(unittest.TestCase):
        def test_row_count(self):
            df = from_csv('file_of_known_size.txt')
            self.assertEqual(len(df), 450)

        def test_col_count(self):
            df = from_csv('file_of_known_size.txt')
            self.assertEqual(len(df.columns), 5)

        def test_change_sep(self):
            """
            change the separator to a sign that does not appear
            in the file. then there sould be only one column.
            """
            df = from_csv('file_of_known_size.txt', sep="|")
            self.assertEqual(len(df.columns)), 1)

    if __name__=='__main__':
        unittest.main()


This is a very basic example that does check three different things. It uses
our new tool to load a file of known content into the variable ``df``.

.. _contrib_docstrings:

Add / improve docstrings
========================

.. important::

    If you are not familiar with the numpydoc docstring format, please refer to
    http://numpydoc.readthedocs.io/en/latest/format.html.

The most important parts of a numpydoc docstring are shown in the example below. Please make
sure, that your docstring always contains the `main description`, `parameters` and `returns`.

.. code-block:: python
    :linenos:

    @accept(path=(str, TextIOWrapper), sep=str)
    def from_csv(path, sep=','):
    r"""short descriptive tile

    After a short title, give a few sentences of explanation. What does this
    Method do and how is it intended to be used?

    Parameters
    ----------
    path : str, TextIOWrapper
        The parameters can also get a full description about their meaning
        possible values. Please be as extensive as necessary here.
        Note the whitespace between the parameter name and the (list) of
        accepted types.
    sep : str, optional
        In case an argument is optional, you can indicate this by the
        optional keyword after the type.

    Returns
    -------
    pandas.DataFrame

    Notes
    -----

    The first description at the top should be a rather technical description.
    The optional Notes section can be added and used to inform the user about
    the background of the function or further readings.
    For this purpose you can also include references[1]_ into your Notes.
    In the documentations, these will be rendered in the Reference section.

    And last but not least you can also input some math:

    .. math:: a^2 + b^2 = c^2

    References
    ----------

    ..  [1] Python, M., Chapman, G., Cleese, J., Gilliam, T., Jones, T.,
        Idle, E., & Palin, M. (2000). the Holy Grail. EMI Records.

    Examples
    --------

    >>> from_csv('file.txt').size
    (220201, 5)

    """
    ...


.. note::

    You should only add short and descriptive examples into the docstring itself. Make use of the
    :ref:`Examples section <contrib_examples>` of this documentation.


.. _contrib_examples:

Enhance the Examples
====================

.. todo::

    write this section


.. _contrib_pull:

Create a Pull Request
=====================

.. important::

    If you are not familiar with Pull Requests, please refer to
    https://help.github.com/articles/about-pull-requests.

The best scenario for a pull request would be one that includes the new tool / enhancement, a
proper docstring, unittests and a new example. However, we will also accept a pull request
including only a tool and a docstring. In these cases, please provide a proper description in the
pull request message in order to make it possible for others to add missing content.

Beside a good description, a descriptive title is vital. Please state what you actually want to
contribute in the pull request title. For the examples produced in this guide a descriptive title
would be something like: `Added from_csv tool for reading files`.

.. note::

    If your contribution does only contain minor changes like PEP8 fixes, typos and small
    bugfixes, you can of course pull request these changes without examples and unittests.

And finally, I am really looking forward to your contributions and thanks in advance!