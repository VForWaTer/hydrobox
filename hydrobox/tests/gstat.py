import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from hydrobox.toolbox import variogram

class TestVariogram(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.c = np.random.gamma(20, 10, (30, 2))
        np.random.seed(42)
        self.v = np.random.normal(10, 5, 30)

    def test_default_no_plot(self):
        b, e, y = variogram(self.c, self.v, effective_range=37., sill=21.,
                      plot=False)

        # test
        assert_array_almost_equal(
            [3.82, 7.64, 11.46, 15.29, 19.11, 22.93, 26.75, 30.57, 34.39,
             38.21, 42.03, 45.86, 49.68, 53.5, 57.32],
            b, decimal=2)
        assert_array_almost_equal(
            [10.16, 12.3, 0.58, 18.52, 21.74, 41.21, 13.74, 12.25, 20.49,
             18.87, 22.72, 16.34, 20.74, 28.57, 0.],
            e, decimal=2
        )



if __name__ == '__main__':
    unittest.main()
