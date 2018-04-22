import unittest
import numpy as np
import pandas as pd
from numpy.testing import assert_array_almost_equal
from hydrobox.discharge.catchment import flow_duration_curve, regime

# some result container
PROBCALC = np.array([0.04761905, 0.0952381, 0.14285714, 0.19047619, 0.23809524, 0.28571429,  0.33333333,
                     0.38095238, 0.42857143, 0.47619048, 0.52380952, 0.57142857,  0.61904762,  0.66666667,
                     0.71428571, 0.76190476, 0.80952381, 0.85714286, 0.9047619,  0.95238095])

MULTI_PROBCALC = np.array([[0.04761905,  0.04761905,  0.04761905],
                           [0.0952381,  0.0952381,  0.0952381],
                           [0.14285714, 0.14285714, 0.14285714],
                           [0.19047619, 0.19047619, 0.19047619],
                           [0.23809524, 0.23809524, 0.23809524],
                           [0.28571429, 0.28571429, 0.28571429],
                           [0.33333333, 0.33333333, 0.33333333],
                           [0.38095238, 0.38095238, 0.38095238],
                           [0.42857143, 0.42857143, 0.42857143],
                           [0.47619048, 0.47619048, 0.47619048],
                           [0.52380952, 0.52380952, 0.52380952],
                           [0.57142857, 0.57142857, 0.57142857],
                           [0.61904762, 0.61904762, 0.61904762],
                           [0.66666667, 0.66666667, 0.66666667],
                           [0.71428571, 0.71428571, 0.71428571],
                           [0.76190476, 0.76190476, 0.76190476],
                           [0.80952381, 0.80952381, 0.80952381],
                           [0.85714286, 0.85714286, 0.85714286],
                           [0.9047619, 0.9047619, 0.9047619],
                           [0.95238095, 0.95238095, 0.95238095]]
                          )

REGIME_MEDIAN = np.array([2.98892946, 3.29395953, 3.6583898, 3.45867616, 3.74621256, 3.6528729, 3.39625957,
                          4.05270697, 3.22589666, 3.18676455, 3.08711612, 3.71620022])

REGIME_MEAN = np.array([3.5336286, 3.77460559, 3.89284876, 4.26961426, 4.65499045, 4.03412380,  4.11861575,
                        4.72649556, 4.34447189, 3.75299656, 3.78642528, 4.2730813])

REGIME_NORMALIZED_MEDIAN = np.array([0.87205178, 0.96104753, 1.06737392, 1.00910535, 1.09299714,
                                     1.06576430, 0.99089465, 1.18242012, 0.94118947, 0.92977226,
                                     0.90069878, 1.08424072])
REGIME_NORMALIZED_MEAN = np.array([0.86252861, 0.92134903, 0.95021118, 1.04217643, 1.13624347,
                                   0.98469522, 1.00531898, 1.15369726, 1.06044854, 0.91607445,
                                   0.92423412, 1.0430227])

REGIME_QUANTILES = np.array([[2.98892946, 1.716014, 2.7438941, 3.36943366, 4.92019676],
                            [3.29395953, 1.86332905, 2.58050715, 4.04496950, 5.74265783],
                            [3.65838980, 1.75722127, 2.93123317, 4.22219928, 5.59038127],
                            [3.45867616, 1.73668189, 2.76901890, 4.21388916, 6.41038660],
                            [3.74621256, 2.11604735, 3.07424791, 4.82633494, 6.93547862],
                            [3.65287290, 1.76783106, 3.03289193, 4.17600437, 5.77479856],
                            [3.39625957, 1.92886187, 3.00034985, 3.97661571, 6.16182702],
                            [4.05270697, 2.23409483, 3.42534304, 4.80208306, 7.26159780],
                            [3.22589666, 1.63461114, 3.05938285, 3.94513106, 6.78734532],
                            [3.18676455, 1.60000531, 2.65241603, 3.65676955, 5.98111450],
                            [3.08711612, 1.64122269, 2.61680947, 3.77372665, 5.80221639],
                            [3.71620022, 1.69847299, 3.05755018, 4.41203946, 6.1562861]])

REGIME_QUANTILES_NORMALIZED = np.array([[0.87205178, 0.98229053, 0.92518105, 0.81971643, 0.81074967],
                                       [0.96104753, 1.06661746, 0.87009054, 0.98406091,  0.94627474],
                                       [1.06737392, 1.00587864, 0.98834768, 1.02717740,  0.92118262],
                                       [1.00910535, 0.99412136, 0.93365258, 1.02515571,  1.05630304],
                                       [1.09299714, 1.21127991, 1.03656913, 1.17415163,  1.14282767],
                                       [1.06576430, 1.01195195, 1.02262479, 1.01593909,  0.95157089],
                                       [0.99089465, 1.10413013, 1.01165232, 0.96743178,  1.01534541],
                                       [1.18242012, 1.27885332, 1.15495072, 1.16825163,  1.19656556],
                                       [0.94118947, 0.93569344, 1.03155695, 0.95977219,  1.11841827],
                                       [0.92977226, 0.91588417, 0.89433665, 0.88961955,  0.98556762],
                                       [0.90069878, 0.93947807, 0.88233089, 0.91807290,  0.95608880],
                                       [1.08424072, 0.97224961, 1.03093902, 1.07336175,  1.01443238]])

REGIME_QUANTILES_MEAN = np.array([[3.5336286, 1.716014, 2.7438941, 3.36943366, 4.92019676],
                                  [3.77460559, 1.86332905, 2.58050715, 4.04496950, 5.74265783],
                                  [3.89284876, 1.75722127, 2.93123317, 4.22219928, 5.59038127],
                                  [4.26961426, 1.73668189, 2.76901890, 4.21388916, 6.41038660],
                                  [4.65499045, 2.11604735, 3.07424791, 4.82633494, 6.93547862],
                                  [4.03412380, 1.76783106, 3.03289193, 4.17600437, 5.77479856],
                                  [4.11861575, 1.92886187, 3.00034985, 3.97661571, 6.16182702],
                                  [4.72649556, 2.23409483, 3.42534304, 4.80208306, 7.26159780],
                                  [4.34447189, 1.63461114, 3.05938285, 3.94513106, 6.78734532],
                                  [3.75299656, 1.60000531, 2.65241603, 3.65676955, 5.98111450],
                                  [3.78642528, 1.64122269, 2.61680947, 3.77372665, 5.80221639],
                                  [4.27308130, 1.69847299, 3.05755018, 4.41203946, 6.15628610]])



class TestFlowDurationCurve(unittest.TestCase):

    def setUp(self):
        """
        Set up some random data.

        :return:
        """
        np.random.seed(42)
        self.gamma = np.random.gamma(2, 2, size=20)
        self.multi_gamma = np.random.gamma(2, 2, size=(20, 3))

    def test_probability_calculation(self):
        assert_array_almost_equal(flow_duration_curve(self.gamma, plot=False), PROBCALC)

    def test_probability_inverse(self):
        assert_array_almost_equal(flow_duration_curve(self.gamma, plot=False, non_exceeding=False), PROBCALC[::-1])

    def test_multi_probablility_calculation(self):
        assert_array_almost_equal(flow_duration_curve(self.multi_gamma, plot=False), MULTI_PROBCALC)

    def test_multi_probability_inverse(self):
        assert_array_almost_equal(
            flow_duration_curve(self.multi_gamma, plot=False, non_exceeding=False),
            MULTI_PROBCALC[::-1]
        )


class TestRegime(unittest.TestCase):

    def setUp(self):
        """
        Set up some random data.

        :return:
        """
        np.random.seed(42)
        self.series = pd.Series(
            index=pd.date_range('20000101', '20021231', freq='D'),
            data=np.random.gamma(2, 2, 3*365 + 1))

    def test_aggregation_median(self):
        """
        Test Regime Funtction with Median

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False).flatten(), REGIME_MEDIAN)

    def test_aggregation_mean(self):
        """
        Test Regime Funtction with Mean

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False, agg='nanmean').flatten(), REGIME_MEAN)

    def test_normalized_median(self):
        """
        Test Regime Funtction with Median and normalized values

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False, normalize=True).flatten(),
                                  REGIME_NORMALIZED_MEDIAN)

    def test_normalized_mean(self):
        """
        Test Regime Funtction with Mean and normalized values

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False, normalize=True, agg='nanmean').flatten(),
                                  REGIME_NORMALIZED_MEAN)

    def test_quantiles_calculation(self):
        """
        Test Regime Funtction with Quantiles

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False,
                                         percentiles=4).values,
                                  REGIME_QUANTILES)

    def test_quantiles_normalized(self):
        """
        Test Regime Funtction with normalized Quantiles

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False, percentiles=4, normalize=True).values,
                                  REGIME_QUANTILES_NORMALIZED)

    def test_quantiles_mean(self):
        """
        Test Regime Funtction with Quantiles and Mean Function

        :return:
        """
        assert_array_almost_equal(regime(self.series, plot=False, percentiles=4, agg='nanmean').values,
                                  REGIME_QUANTILES_MEAN)

if __name__ == '__main__':
    unittest.main()
