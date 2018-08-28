import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from hydrobox.toolbox import variogram_model

class TestVariogram(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.c = np.random.gamma(20, 10, (30, 2))
        np.random.seed(42)
        self.v = np.random.normal(10, 5, 30)

        # results
        self.b = [3.82, 7.64, 11.46, 15.29, 19.11, 22.93, 26.75, 30.57, 34.39,
             38.21, 42.03, 45.86, 49.68, 53.5, 57.32]
        self.e = [10.16, 12.3, 0.58, 18.52, 21.74, 41.21, 13.74, 12.25, 20.49,
             18.87, 22.72, 16.34, 20.74, 28.57, 0.]

    def test_default_no_plot(self):
        b, e, y = variogram_model(self.c, self.v, effective_range=37., sill=21.,
                                  plot=False)

        # test
        assert_array_almost_equal(self.b, b, decimal=2)
        assert_array_almost_equal(self.e, e, decimal=2)

    def test_matern_function(self):
        b, e, y = variogram_model(self.c, self.v, effective_range=37., sill=21.,
                                  nugget=3., plot=False, model='matern', s=15.)

        # test
        # experimental part should not have changed
        assert_array_almost_equal(self.b, b, decimal=2)
        assert_array_almost_equal(self.e, e, decimal=2)

        # check function
        assert_array_almost_equal(
            y[[1, 5, 8, 13, 40, 50, 60, 80, 90]],
            [4.21, 5.61, 6.91, 9.4, 20.84, 22.61, 23.45, 23.94, 23.98],
            decimal=2
        )

    def test_variogram_plot(self):
        # run without plot first:
        b, e, y = variogram_model(self.c, self.v, effective_range=37., sill=21.,
                                  nugget=3., plot=False, model='matern', s=15.)

        # run with plot
        fig = variogram_model(self.c, self.v, effective_range=37., sill=21.,
                              nugget=3., plot=True, model='matern', s=15.)
        # dig out the arrays
        ax = fig.axes[0]
        exp_line, mod_line = ax.get_lines()

        # test experimental scatter plot
        assert_array_almost_equal(b, exp_line.get_data()[0], decimal=6)
        assert_array_almost_equal(e, exp_line.get_data()[1], decimal=6)

        # test model function
        assert_array_almost_equal(y, mod_line.get_data()[1], decimal=6)




if __name__ == '__main__':
    unittest.main()
