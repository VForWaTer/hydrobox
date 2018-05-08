import unittest

import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal

from hydrobox.toolbox import linear_regression

SLOPE = np.array([[np.NaN, 0.91805201, 2.78405077, 6.47730137,
                   -0.95212053],
                  [0.84301931, np.NaN, 2.49724175, 5.9976942, -0.86178828],
                  [0.30928324, 0.30211312, np.NaN, 2.21419697, -0.31145363],
                  [0.13842524, 0.13958388, 0.42594958, np.NaN, -0.14156071],
                  [-0.24798999, -0.24444017, -0.73022449, -1.72529667, np.NaN]])

INTERCEPT = np.array([[np.NaN, -0.05160877, 1.38133079, 1.58610304,
                       0.83809328],
                      [0.11843668, np.NaN, 1.6731034, 2.21751166, 0.74026891],
                      [-0.3811706, -0.44342045, np.NaN, -1.36873584,
                       1.24013445],
                      [-0.18529185, -0.26838765, 0.71403273, np.NaN,
                       1.05095964],
                      [0.46102946, 0.38040405, 2.68566021, 4.63450378, np.NaN]])

RVALUE = np.array([[np.NaN, 0.87973608, 0.92793331, 0.94690125,
                    -0.48591806],
                   [0.87973608, np.NaN, 0.86859052, 0.91497618, -0.45897241],
                   [0.92793331, 0.86859052, np.NaN, 0.97115203, -0.47689733],
                   [0.94690125, 0.91497618, 0.97115203, np.NaN, -0.49420059],
                   [-0.48591806, -0.45897241, -0.47689733, -0.49420059,
                    np.NaN]])

PVALUE = np.array([[np.NaN, 2.07484743e-33, 8.61998829e-44,
                    4.31913912e-50,
                    2.97788702e-07],
                   [2.07484743e-33, np.NaN, 1.20754364e-31, 2.07235415e-40,
                    1.56492402e-06],
                   [8.61998829e-44, 1.20754364e-31, np.NaN, 8.02787469e-63,
                    5.27264479e-07],
                   [4.31913912e-50, 2.07235415e-40, 8.02787469e-63, np.NaN,
                    1.73677007e-07],
                   [2.97788702e-07, 1.56492402e-06, 5.27264479e-07,
                    1.73677007e-07,
                    np.NaN]])

STDERR = np.array([[np.NaN, 0.0501208, 0.11296935, 0.22217259, 0.17299337],
                   [0.04602441, np.NaN, 0.14391395, 0.26718587, 0.16851331],
                   [0.01254989, 0.01741053, np.NaN, 0.05492039, 0.05798612],
                   [0.00474801, 0.0062182, 0.01056515, np.NaN, 0.02515475],
                   [0.04505798, 0.04779761, 0.13595246, 0.30657808, np.NaN]])


class TestLinearRegression(unittest.TestCase):
    def setUp(self):
        np.random.seed(2409)
        noise = np.random.normal(0, 1, size=(100, 5))
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100) + 1
        z = np.linspace(1, 0, 100)
        self.df = pd.DataFrame(data=np.array([
            x**2 + 0.1*noise[:, 0],
            x**3 + 0.1*noise[:, 1],
            y**2 + 0.2*noise[:, 2],
            y**3 + 0.15*noise[:, 3],
            z + 0.5*noise[:, 4]
        ]).T)

    def test_default(self):
        result = linear_regression(self.df[[0]], self.df[[1]])
        expected = dict(slope=0.918052,
                        intercept=-0.051608,
                        rvalue=0.879736,
                        pvalue=2.074847426211272e-33,
                        stderr=0.050120)
        for exp, res in zip(expected.values(), result.values()):
            self.assertAlmostEqual(exp, res, places=4)

    def test_df_input(self):
        self.assertEqual(
            linear_regression(self.df[[0]], self.df[[1]]),
            linear_regression(df=self.df[[0, 1]])
        )

    def test_mulit_slope(self):
        assert_almost_equal(
            linear_regression(df=self.df)[0],
            SLOPE, decimal=6
        )

    def test_mulit_intercept(self):
        assert_almost_equal(
            linear_regression(df=self.df)[1],
            INTERCEPT, decimal=6
        )

    def test_mulit_rvalue(self):
        assert_almost_equal(
            linear_regression(df=self.df)[2],
            RVALUE, decimal=6
        )

    def test_mulit_pvalue(self):
        assert_almost_equal(
            linear_regression(df=self.df)[3],
            PVALUE, decimal=6
        )

    def test_mulit_stderr(self):
        assert_almost_equal(
            linear_regression(df=self.df)[4],
            STDERR, decimal=6
        )


if __name__ == '__main__':
    unittest.main()
