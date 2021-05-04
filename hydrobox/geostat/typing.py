from typing import Union, Callable, Literal
import numpy as np

# some typings
Estimator = Union[
    Literal['matheron','cressie', 'dowd''genton', 'entropy', 'minmax', 'percentile'], 
    Callable[[np.ndarray], float]
]

Model = Union[
    Literal['spherical', 'exponential', 'gaussian', 'matern', 'cubic', 'stable'],
    Callable[[float, float], float],
    Callable[[float, float, float], float],
    Callable[[float, float, float, float], float]
]

DistFunc = Literal[
    'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice',
    'euclidean', 'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis',
    'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
    'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'],

BinFunc = Literal['even', 'uniform', 'sqrt', 'scott', 'sturge', 'kmean', 'ward', 'fd', 'doane']

FitMethod = Literal['trf', 'lm', 'ml', 'custom']

FitSigma = Union[None, np.ndarray, Literal['linear', 'sqrt', 'sq', 'exp']]

Maxlag = Union[None, Literal['mean', 'median'], int, float]