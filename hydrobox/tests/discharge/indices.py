import unittest

import numpy as np
import pandas as pd

from hydrobox.toolbox import indices


class TestRichardBaker(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.x = np.random.normal(5, .5, size=10)

    def test_default(self):
        self.assertAlmostEqual(
            indices.richards_baker(self.x),
            0.0949901,
            places=6
        )

    def test_with_gamma(self):
        np.random.seed(2409)
        x = np.random.gamma(5,.5, size=1000)
        self.assertAlmostEqual(indices.richards_baker(x), 0.4890978, places=6)

    def test_wrong_value(self):
        self.assertNotAlmostEqual(indices.richards_baker(self.x), 0.4890978,
                                  places=6)

    def test_series(self):
        series = pd.Series(data=self.x)
        self.assertAlmostEqual(
            indices.richards_baker(series),
            0.0949901,
            places=6
        )


if __name__ == '__main__':
    unittest.main()
