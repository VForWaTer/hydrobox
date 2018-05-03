import unittest

import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal
from pandas.testing import assert_series_equal, assert_index_equal

from hydrobox.toolbox import merge


class TestMerge(unittest.TestCase):
    def setUp(self):
        self.s1 = pd.Series(data=[1, 2, 3])
        self.s2 = pd.Series(data=[4, 5.5])
        self.s3 = pd.Series(data=[7, 9.5, 4.5, 2])
        self.dtindex = pd.date_range('201309241100', freq='2H', periods=4)

    def test_default(self):
        assert_almost_equal(
            merge(self.s1, self.s2, self.s3).values,
            np.array(
                [[1., 4., 7.], [2., 5.5, 9.5],
                 [3., np.nan, 4.5], [np.nan, np.nan, 2.]])
            , decimal=1
        )

    def test_dropna(self):
        assert_almost_equal(
            merge(self.s1, self.s2, self.s3, dropna=True).values,
            np.array([[1., 4., 7.], [2., 5.5, 9.5]]),
            decimal=1
        )

    def test_index_mismatch(self):
        with self.assertRaises(ValueError):
            s = self.s3.copy()
            s.index = self.dtindex
            merge(self.s1, self.s2, s)

    def test_pass_no_series(self):
        self.assertIsNone(merge())

    def test_pass_only_one_series(self):
        assert_series_equal(self.s1, merge(self.s1))

    def test_datetimeindex(self):
        s1 = self.s1.copy()
        s2 = self.s2.copy()
        s3 = self.s3.copy()

        s1.index = self.dtindex[1:]
        s2.index = self.dtindex[[1,3]]
        s3.index = self.dtindex

        # correct amount of elements
        self.assertEqual(merge(s1, s2, s3).size, 12)
        self.assertEqual(merge(s1, s2, s3, dropna=True).size, 6)

        # check index
        assert_index_equal(merge(s1, s2, s3, dropna=True).index,
                           pd.DatetimeIndex(
                               ['2013-09-24 13:00:00', '2013-09-24 17:00:00'],
                               dtype='datetime64[ns]', freq='4H')
                           )


if __name__ == '__main__':
    unittest.main()
