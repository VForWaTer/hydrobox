"""
This is the main toolbox file.

Here, all major functions will be imported at top level.
"""
from .discharge.catchment import flow_duration_curve, regime
from .discharge import indices
from .signal import simplify
from .preprocessing.scale import aggregate, cut_period
from .preprocessing.union import merge
from .stats import moving_window, linear_regression
from . import io
from . import stats