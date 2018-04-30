"""
The optimize module of the signal processing routine implements some algorithms
for optimizing and simplifying environmental signals under an applied
environmental science or hydrologist perspective.
"""
import numpy as np
import pandas as pd

from hydrobox.utils.decorators import accept


@accept(
    x=(np.ndarray, pd.Series, pd.DataFrame),
    flatten=bool,
    threshold=(int, float)
)
def simplify(x, flatten=True, threshold=0):
    """Simplify signal
    
    An given input is simplified by reducing the amount of nodes representing 
    the signal. Whenever node[n+1] - node[n] <= threshold, no information 
    gain is assumed between the two nodes. Thus, node[n+1] will be removed.

    In case flatten is True, noise in the signal will be flattened as well. 
    This is done by removing node[n + 1] in case node[n] and node[n + 1] hold 
    the same value. In case the underlying frequency in the noise is higher 
    than one time step or the amplitude is higher than the sensor precision, 
    this method will not assume the value change as noise. In these cases a 
    filter needs to be applied first.
    
    Parameters
    ----------
    x : numpy.ndarray, pandas.Series, pandas.DataFrame
        numpy.array of signal
    flatten : bool  
        Specify if a 1 frequence 1 amplitude change in signal be flattened 
        out as assumed noise.
    threshold : int, float 
        value threshold at which a difference in signal is assumed
        
    Returns
    -------
    numpy.ndarray

    """
    # Turn Series and DataFrame instances to a numpy array
    if isinstance(x, (pd.Series, pd.DataFrame)):
        arr = x.values
    else:
        arr = x

    if arr.ndim > 1:
        raise NotImplementedError

    # remove the nodes without a gain of information
    simple = arr[np.where(np.abs(np.diff(arr)) > threshold)]

    # build the remove mask for noise, if not flatten do not remove anything
    if flatten:
        # The first and last element are never removed (False)
        remove_mask = np.concatenate((
            [False],
            np.fromiter((float(simple[i]) == float(simple[i - 2]) for i in range(2, len(simple))), dtype=bool),
            [False]
        ))
    else:
        remove_mask = np.zeros(simple.shape, dtype=bool) * False

    return simple[~remove_mask]
