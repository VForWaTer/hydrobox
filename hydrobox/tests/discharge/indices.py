import unittest

import numpy as np

from hydrobox.toolbox import indices


class TestIndices(unittest.TestCase):
    def setUp(self):
        pass

    def test_richards_baker(self):
        np.random.seed(42)
        x = np.random.normal(5,.5, size=10)
        self.assertAlmostEqual(indices.richards_baker(x), 0.0949901, places=6)

        np.random.seed(2409)
        x2 = np.random.gamma(5,.5, size=1000)
        self.assertAlmostEqual(indices.richards_baker(x2), 0.4890978, places=6)

        self.assertNotAlmostEqual(indices.richards_baker(x), 0.4890978,
                                  places=6)



if __name__ == '__main__':
    unittest.main()
