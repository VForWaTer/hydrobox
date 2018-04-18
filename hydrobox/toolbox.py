"""
This is the main toolbox file.

Here, all major functions will be imported at top level.
"""
from .discharge.stats import flow_duration_curve, regime
from .signal import simplify
from .sample import rf, random
from . import io
