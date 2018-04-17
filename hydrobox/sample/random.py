"""

"""
from hydrobox.utils.decorators import accept
import numpy as np

@accept(arr=np.ndarray, size=int, seed=('None', int), replace=bool)
def choice(arr, size=100, seed=None, replace=True):
    """
    Returns :param size: samples from :param arr: by randomly selecting coordinates on all axes.
    If replace is True, coordinate duplicates will be replaced until all coordinates are unique.
    :param replace: will be set to False automatically if :py: `any([size > N for N in arr.shape])`.
    This would result in an inifite loop.

    Parameters
    ~~~~~~~~~~
    :param arr:         numpy.ndarray, n-dimensional sample array
    :param size:        int, number of coordinates to be chosen
    :param seed:        int, seed for numpy.random.seed
    :param replace:     bool, if True, coordinate duplicates will be replaced iteratively
    :return:
    """
    # set the seed
    np.random.seed(seed)

    # auto-deactivate replace
    if any([size > n for n in arr.shape]):
        print('size of %d is too big for input of shape %s. At least one axis does not have enough samples: ' %
              (size, str(arr.shape)))
        replace = False

    # get the index
    def _choice(shape, size):
        return list(zip(*(np.random.randint(_, size=size) for _ in shape)))

    idx = _choice(arr.shape, size=size)

    while replace:
        # check for duplicates
        idx = np.vstack({tuple(a) for a in idx})
        if len(idx) == size:
            break
        else:
            idx = np.append(idx, _choice(arr.shape, size=size - len(idx)))

    return idx, arr[tuple(idx.T)]
