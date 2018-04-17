"""
The rf module implements different functions for generating random fields.
Beside the numpy implementation of these fields, auxiliary functions for adding them to a HydroFrame instance
or returning them as a DataSource are included.
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def fftIndgen(n):
    """

    :param n:
    :return:
    """
    a = np.arange(0, int(n/2+1), 1)
    b = np.negative(np.arange(int(n/2), 1, -1))
    return np.concatenate((a,b), axis=0)


def gaussian2D(alpha=-3, size=(100, 100), dist=np.random.normal, seed=None, feature_range=(0,1)):
    """

    :param pk:
    :param size:
    :param dist:
    :param seed:
    :param feature_range:
    :return:
    """
    if isinstance(alpha, (int, float)):
        pk = lambda k: k**alpha
    elif callable(alpha):
        pk = alpha
    else:
        raise ValueError('alpha has to be a callable returning k(alpha) or alpha which will be used as k: k**alpha. alpha should be negative.')

    # set the seed
    np.random.seed(seed)

    # define the pk2 function
    def pk2(kx,ky):
        if kx == 0 and ky == 0:
            return 0.0
        return np.sqrt(pk(np.sqrt(kx**2 + ky**2)))

    # create the noise
    # the noise is the 2D fourier transformation of a sample from the given distribution
    noise = np.fft.fft2(dist(size=size))

    # create the amplitude
    amplitude = np.zeros(size)

    for i, kx in enumerate(fftIndgen(size[0])):
        for j, ky in enumerate(fftIndgen(size[1])):
            amplitude[i,j] = pk2(kx, ky)

    #return the inverse fourier transformation of the product for amplitude and noise
    out = np.fft.ifft2(noise * amplitude)

    # use the original values or rescale by min and max
    if feature_range is None:
        return out.real
    else:
        return MinMaxScaler(feature_range=feature_range).fit_transform(out.real, y=out.shape)
