import unittest

import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal
from numpy.testing import assert_almost_equal

from hydrobox.toolbox import aggregate


class TestAggregate(unittest.TestCase):
    def setUp(self):
        np.random.seed(1337)
        self.series = pd.Series(
            data=np.random.gamma(15,3.5, size=1000),
            index=pd.date_range('201309241100', freq='15min', periods=1000)
        )

    def test_default(self):
        assert_almost_equal(
            aggregate(self.series, '3D').values,
            pd.Series(data=np.array([51.876872, 53.429440, 53.03754, 52.357760])),
            decimal=5
        )

    def test_callable(self):
        f = lambda x: np.nanmedian(x)
        assert_almost_equal(
            aggregate(self.series, '3D', func=f).values,
            pd.Series(data=np.array([51.471671, 51.989241, 52.215048, 50.50436])),
            decimal=5
        )

    def test_raise_on_non_timeseries_input(self):
        s = pd.Series(data=self.series.values)
        with self.assertRaises(ValueError):
            aggregate(s, by='5min')

    def test_aggregate_by_none(self):
        self.assertAlmostEqual(
            aggregate(self.series, by=None),
            52.72368669, places=6
        )

    def test_aggregate_by_all(self):
        self.assertAlmostEqual(
            aggregate(self.series, by='all'),
            52.72368669, places=6
        )


if __name__ == '__main__':
    unittest.main()
