"""
The optimize module of the signal processing routine implements some algorithms for optimizing simplifying environmental
signals under an applied environmental science or hydrologist perspective.
"""
import numpy as np

from hydrobox.utils.decorators import accept


@accept(x=np.ndarray, flatten=bool, threshold=(int, float))
def simplify(x, flatten=True, threshold=0):
    """
    An given input is simplyfied by reducing the amount of nodes representing the signal.
    Whenever node[n+1] - node[n] <= threshold, no information gain is assumed between the
    two nodes. node[n+1] will be removed.

    In case flatten is True, noise in the signal will be flattened as well. This is done
    by removing node[n + 1] in case node[n] and node[n + 1] hold the same information.

    :param x:               numpy.array of signal
    :param flatten:         bool, flatten out noise
    :param threshold:       int,float threshold at which a difference in signal is assumed
    :return: :py:mod::`numpy`.:py:class::`ndarray` of simplified signal
    """
    if x.ndim > 1:
        raise NotImplementedError

    # remove the nodes without a gain of information
    simple = x[np.where(np.abs(np.diff(x)) > threshold)]

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
