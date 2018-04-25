# HydroBox

[![Build Status](https://travis-ci.org/mmaelicke/hydrobox.svg?branch=master)](https://travis-ci.org/mmaelicke/hydrobox)
[![Documentation Status](https://readthedocs.org/projects/hydrobox/badge/?version=latest)](http://hydrobox.readthedocs.io/en/latest?badge=latest)

**The HydroBox is mainly a toolbox used in the [V-FOR-WaTer](https://vforwater.de) Project. It will be expanded to
serve general hydrological data exploration with a future release.**

<div class="alert alert-info>The full documentation can be found at: http://hydrobox
.readthedocs.io</div>

The HydroBox package is a toolbox for hydrological data analysis developed at the
[Chair of Hydrology](https://hyd.iwg.kit.edu/english/index.php) at the
[Karlsruhe Institute of Technology (KIT)](https://kit.edu/english/index.php).
The HydroBox has a submodule called toolbox, which is a collection of functions and classes that accept common
numpy and pandas input formats and wrap around scipy functionality. This way can:

- speed up common hydrological data analysis tasks
- integrate fully with custom numpy/pandas/scipy code


## Installation

Install the Hydrobox using pip. The latest version on [PyPI](https://pypi.python.org/pypi/hydrobox) can
be installed using pip:

```bash
pip install hydrobox
```

There might be a more recent version on GitHub available. This can be installed like:

```bash
git clone https://github.com/mmaelicke/hydrobox.git
cd hydrobox
pip install -r requirements.txt
pip install -e .
```
    

## Tests

The hydrobox module uses unittest for setting up some test. All the different TestCases are grouped into
different submodules. Each of them is executable and can run the unit tests for this part of the toolbox.
In case you just want to run the test of the decorators, run just that script in the tests folder.

```bash
python /path/to/hydrobox/tests/decorators.py 

    ...
    Ran 5 tests in 0.081s

    OK
```


Alternatively, nose is integrated to run either `nosetests` in the repository root
or run the setup.py with the `test` keyword like:

```bash
python setup.py test

    ...
    ----------------------------------------------------------------------
    Ran 10 tests in 1.792s

    OK

```


## Getting Started


Most of the tools are available either as a function or a class importet into the `toolbox` module.
Most tools accept numpy types as input and will use them for return, as well. This way the HydroBox should
integrate with your common data analysis tools. The non-plotted flow duration curve could for example be used
like:

```python
from hydrobox.toolbox import flow_duration_curve
import numpy as np

# set the seed and generate random data
np.random.seed(42)
gamma = np.random.gamma(2,2,size=20)

# run the flow duration curve without plotting
probs = flow_duration_curve(gamma, plot=False)

print('Type:', type(probs))
print(probs)
```

```bash
Type: numpy.ndarray
array([0.04761905, 0.0952381, 0.14285714, 0.19047619, 0.23809524, 0.28571429,  0.33333333,
    0.38095238, 0.42857143, 0.47619048, 0.52380952, 0.57142857,  0.61904762,  0.66666667,
    0.71428571, 0.76190476, 0.80952381, 0.85714286, 0.9047619,  0.95238095])
```

