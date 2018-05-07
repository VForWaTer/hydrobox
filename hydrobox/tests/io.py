import unittest
from datetime import datetime as dt

import pandas as pd
from pandas.testing import assert_series_equal, assert_index_equal

from hydrobox.io.random import timeseries_from_distribution

DEFAULT_ARGS = pd.Series(
    index=pd.date_range(start='200001011130', periods=10, freq='D'),
    data=[22.589431, 18.486253, 17.913554, 17.913652, 30.909718, 24.508842, 16.558495, 22.907162, 20.877284, 9.709636]
)
NORMAL_DISTRIBUTION = pd.Series(
    index=pd.date_range(start='200001011130', periods=10, freq='D'),
    data=[10.99342831, 9.7234714, 11.29537708, 13.04605971, 9.53169325, 9.53172609, 13.15842563, 11.53486946,
          9.06105123, 11.08512009]
)
DISTRIBUTION_ARGS = pd.Series(
    index=pd.date_range(start='200001011130', periods=10, freq='D'),
    data=[3.248357, 2.930867, 3.323844, 3.761514, 2.882923, 2.882931, 3.789606, 3.383717, 2.765262, 3.271280]
)

SEED_2409 = pd.Series(
    index=pd.date_range(start='200001011130', periods=10, freq='D'),
    data=[15.0593175, 22.25531155, 22.97909144, 35.0290098, 17.74052049, 19.89981716, 23.79123233, 23.55748969,
          14.38911486, 12.77600287]
)


class TestTimeSeriesFromDistribution(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_args(self):
        assert_series_equal(
            timeseries_from_distribution(seed=42, start='200001011130'),
            DEFAULT_ARGS, check_less_precise=6
        )

    def test_normal_distribution(self):
        assert_series_equal(
            timeseries_from_distribution(distribution='normal',
                                         seed=42, start='200001011130'),
            NORMAL_DISTRIBUTION, check_less_precise=6
        )

    def test_distribution_args(self):
        assert_series_equal(
            timeseries_from_distribution(
                distribution='normal',
                distribution_args=[3, 0.5],
                seed=42,
                start='200001011130'),
            DISTRIBUTION_ARGS, check_less_precise=6
        )

    def test_size(self):
        assert_series_equal(
            timeseries_from_distribution(seed=42, start='200001011130', size=5),
            DEFAULT_ARGS[:5], check_less_precise=6
        )

    def test_seed(self):
        assert_series_equal(timeseries_from_distribution(seed=2409, start='200001011130'),
                            SEED_2409, check_less_precise=6)

    def test_start(self):
        assert_index_equal(
            timeseries_from_distribution(start='20130924').index,
            pd.date_range(start='20130924', periods=10, freq='D')
        )

    def test_start_datetime(self):
        assert_index_equal(
            timeseries_from_distribution(start=dt(2013, 9, 24)).index,
            pd.date_range(start='20130924', periods=10, freq='D')
        )

    def test_start_now(self):
        assert_index_equal(
            timeseries_from_distribution(start='now').index,
            pd.date_range(dt.now().strftime('%Y%m%d%H%M%S'),
                          periods=10, freq='D')
        )

    def test_end(self):
        assert_index_equal(
            timeseries_from_distribution(start=None, end='20130924').index,
            pd.date_range(end='20130924', periods=10, freq='D')
        )

    def test_end_datetime(self):
        assert_index_equal(
            timeseries_from_distribution(start=None, end=dt(2013, 9, 24)).index,
            pd.date_range(end='20130924', periods=10, freq='D')
        )

    def test_end_now(self):
        assert_index_equal(
            timeseries_from_distribution(start=None, end='now').index,
            pd.date_range(end=dt.now().strftime('%Y%m%d%H%M%S'),
                          periods=10, freq='D')
        )

    def test_freq(self):
        assert_index_equal(
            timeseries_from_distribution(start='20130924', freq='3H').index,
            pd.date_range(start='20130924', periods=10, freq='3H')
        )

    def test_import_unkown_func(self):
        with self.assertRaises(ValueError):
            timeseries_from_distribution(distribution='not_importable_func')


if __name__ == '__main__':
    unittest.main()