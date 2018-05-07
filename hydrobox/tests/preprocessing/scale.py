import unittest
from datetime import datetime as dt

import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal
from pandas.testing import assert_index_equal

from hydrobox.toolbox import aggregate, cut_period


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


class TestCutPeriod(unittest.TestCase):
    def setUp(self):
        np.random.seed(1337)
        self.series = pd.Series(
            data=np.random.gamma(14,0.3, size=200),
            index=pd.date_range('201309241100', freq='15min', periods=200)
        )
        np.random.seed(1337)
        self.df = pd.DataFrame(
            data=np.random.gamma(14, 0.3, size=(200, 2)),
            index=pd.date_range('201309241100', freq='15min', periods=200)
        )

    def test_default_series(self):
        assert_index_equal(
            pd.date_range('201309251200', '201309260315', freq='15min'),
            cut_period(self.series, '201309251200', '201309260315').index
        )

    def test_default_df(self):
        assert_index_equal(
            pd.date_range('201309251200', '201309260315', freq='15min'),
            cut_period(self.df, '201309251200', '201309260315').index
        )

    def test_datetime_series(self):
        assert_index_equal(
            pd.date_range('201309251115', '201309251830', freq='15min'),
            cut_period(self.series, dt(2013, 9, 25, 11, 15),
                       dt(2013, 9, 25, 18, 30)).index
        )

    def test_datetime_df(self):
        assert_index_equal(
            pd.date_range('201309251115', '201309251830', freq='15min'),
            cut_period(self.df, dt(2013, 9, 25, 11, 15),
                       dt(2013, 9, 25, 18, 30)).index
        )

    def test_none(self):
        assert_index_equal(self.series.index,
                           cut_period(self.series, None, None).index
                           )
        assert_index_equal(self.df.index,
                           cut_period(self.df, None, None).index
                           )

    def test_pass_no_timeseries(self):
        with self.assertRaises(ValueError):
            cut_period(pd.Series(data=[1, 2, 3]), None, None)


if __name__ == '__main__':
    unittest.main()
