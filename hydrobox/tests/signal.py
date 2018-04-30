import unittest
import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from hydrobox.toolbox import simplify


class TestSimplify(unittest.TestCase):

    def setUp(self):
        self.x = np.array([3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 4.5, 7.8, 4.4, 4.4,
                           4.4, 4.4, 5.3, 4.4, 5.3, 0.1, 0.2, 0.1, 0.2, 0.2,
                           0.2, 0.2, 0.2, 0.5, 0.2, 0.2])
        self.series = pd.Series(data=self.x)

    def test_simplify_without_flatten(self):
        """
        Simplify signal without flatten

        """
        assert_allclose(
            simplify(self.x, flatten=False),
            np.array(
                [3.2, 4.5, 7.8, 4.4, 5.3, 4.4, 5.3, 0.1, 0.2, 0.1, 0.2, 0.5]
            ),
            atol=0.0
        )

    def test_simplify_without_flatte_series(self):
        assert_allclose(
            simplify(self.series, flatten=False),
            np.array(
                [3.2, 4.5, 7.8, 4.4, 5.3, 4.4, 5.3, 0.1, 0.2, 0.1, 0.2, 0.5]
            ),
            atol=0.0
        )

    def test_simplify_with_flatten(self):
        """
        Simplify signal with flatten

        """
        assert_allclose(
            simplify(self.x, flatten=True),
            np.array([3.2, 4.5, 7.8, 4.4, 5.3, 0.1, 0.2, 0.5]),
            atol=0.0

        )

    def test_threshold_non_zero(self):
        """
        Simplify signal with non-zero threshold

        """
        assert_allclose(
            simplify(self.x, threshold=1),
            np.array([3.2, 4.5, 7.8, 5.3]),
            atol=0.0
        )

    def test_notImplementedError(self):
        with self.assertRaises(NotImplementedError):
            simplify(np.vstack((self.x, self.x)))


if __name__ == '__main__':
    unittest.main()
