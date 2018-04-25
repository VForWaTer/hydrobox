import unittest

import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal, assert_frame_equal

from hydrobox.toolbox import moving_window

DF_DEFAULT = pd.DataFrame(data=np.array([[np.NaN, np.NaN],
                                         [np.NaN, np.NaN],
                                         [np.NaN, np.NaN],
                                         [np.NaN, np.NaN],
                                         [0.40399755, 0.49212467],
                                         [0.21197118, 0.42663158],
                                         [0.13082593, -0.26063044],
                                         [-0.16732696, -0.32626055],
                                         [-0.68573575, -0.41689803],
                                         [-0.77344569, -0.80787078]])
                          )
S_DEFAULT = pd.Series(
    data=np.array(
        [np.NaN, np.NaN, np.NaN, np.NaN, 0.45900297, 0.31283275, 0.65632818,
         0.68027741, 0.28177657, 0.43711925])
)

S_WINDOW_3 = pd.Series(data=np.array([np.NaN, np.NaN, 0.33537946,
                                      0.6774847, 0.64552168,
                                      0.35157984, 0.3703075, 0.7041702,
                                      0.62572439, 0.28017346]))

DF_WINDOW_3 = pd.DataFrame(data=np.array([[np.NaN, np.NaN],
                                          [np.NaN, np.NaN],
                                          [0.30341644, 0.38354287],
                                          [0.66424933, 0.68544254],
                                          [0.29186169, 0.35861927],
                                          [0.21544025, 0.28142167],
                                          [-0.23030994, -0.61214998],
                                          [-0.64879108, -0.98043251],
                                          [-0.83192889, -0.72044015],
                                          [-1.21525768, -0.55344797]])
                           )

S_MEDIAN = pd.Series(data=np.array([np.NaN, np.NaN, np.NaN, np.NaN, 0.49671415,
                                    -0.1382643, 0.64768854, 0.76743473,
                                    -0.23413696, 0.54256004])
                     )

DF_MEDIAN = pd.DataFrame(data=np.array([[np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [0.49671415, 0.54256004],
                                        [-0.23415337, 0.54256004],
                                        [-0.23415337, -0.23413696],
                                        [-0.46341769, -0.46572975],
                                        [-0.46947439, -0.46572975],
                                        [-0.90802408, -0.56228753]])
                         )

DF_BOHMAN = pd.DataFrame(data=np.array([[np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [np.NaN, np.NaN],
                                        [0.29004376, 0.30241634],
                                        [0.82807331, 0.5289004],
                                        [-0.06984259, 0.39019186],
                                        [-0.32740473, -0.55116256],
                                        [-0.27777164, -1.36898523],
                                        [-1.20387951, -0.65456591]])
                         )

S_BOHMAN = pd.Series(data=np.array([np.NaN, np.NaN, np.NaN, np.NaN, 0.66507391,
                                    1.0110242, 0.10760837, 0.11854235,
                                    1.06864576, 0.68475003])
                     )


class TestMovingWindow(unittest.TestCase):
    def setUp(self):
        self.series = pd.Series(
            data=[0.49671415, -0.1382643, 0.64768854, 1.52302986, -0.23415337,
                  -0.23413696, 1.57921282, 0.76743473, -0.46947439, 0.54256004])

        self.df = pd.DataFrame(data=np.array([[0.49671415, -0.1382643],
                                              [0.64768854, 1.52302986],
                                              [-0.23415337, -0.23413696],
                                              [1.57921282, 0.76743473],
                                              [-0.46947439, 0.54256004],
                                              [-0.46341769, -0.46572975],
                                              [0.24196227, -1.91328024],
                                              [-1.72491783, -0.56228753],
                                              [-1.01283112, 0.31424733],
                                              [-0.90802408, -1.4123037]])
                               )

    def test_default_series(self):
        # test Series against default behaviour
        assert_series_equal(moving_window(self.series), S_DEFAULT,
                            check_less_precise=6)

        # test DataFrame against default behaviour
        assert_frame_equal(moving_window(self.df), DF_DEFAULT,
                           check_less_precise=6)

    def test_window_size(self):
        # test Series with altered window size
        assert_series_equal(moving_window(self.series, window_size=3),
                            S_WINDOW_3, check_less_precise=6)

        # test DataFrame with altered window size
        assert_frame_equal(moving_window(self.df, window_size=3),
                           DF_WINDOW_3, check_less_precise=6)

    def test_window_type(self):
        # test Series with altered window type
        assert_series_equal(moving_window(self.series, window_type='bohman',
                                          func='mean'), S_BOHMAN,
                            check_less_precise=6)

        # test DataFrame with altered window type
        assert_frame_equal(moving_window(self.df, window_type='bohman',
                                         func='mean'), DF_BOHMAN,
                           check_less_precise=6)


    def test_func_type(self):
        # test Series with altered function
        assert_series_equal(moving_window(self.series, func='median'),
                            S_MEDIAN, check_less_precise=6)

        # test DataFrame with altered function
        assert_frame_equal(moving_window(self.df, func='median'), DF_MEDIAN,
                           check_less_precise=6)

        # test Series with altered callable function
        assert_series_equal(moving_window(self.series, func=np.median),
                            S_MEDIAN, check_less_precise=6)

        # test DataFrame with altered callable function
        assert_frame_equal(moving_window(self.df, func=np.median), DF_MEDIAN,
                           check_less_precise=6)


    def test_fail_on_execption(self):
        with self.assertRaises(ValueError):
            moving_window(self.series, func='unknown')

        with self.assertRaises(AttributeError):
            moving_window(self.series, window_type='bohman', func='median')

if __name__ == '__main__':
    unittest.main()
