"""
Helper functions for getting and setting the plotting backend.

You can use this function to get or set the current 
plotting backend. 

"""
import importlib

ALLOWED_BACKENDS = ['matplotlib', 'bokeh', 'plotly']
AVAILABLE_BACKENDS = []

# check which one is available
for be in ALLOWED_BACKENDS:
    try:
        exec('import %s' % be)
        AVAILABLE_BACKENDS.append(be)
    except ModuleNotFoundError:
        continue


def plotting_backend(backend=None):
    """
    Set a new or get the current plotting backend.

    Parameters
    ----------
    backend : str, None
        If `None` the current plotting backend will be returned.
        If string, the plotting backend will be set to the given string.
    
    Raises
    ------
    ValueError : If `backend` is a string but not in ['matplotlib', 'bokeh', 'plotly']
    AttributeError : If `backend` is neither str or None

    """
    # need to import at runtime to avoid circular imports
    import hydrobox

    if backend is None:
        return hydrobox.__plot_backend__
    elif isinstance(backend, str):
        if backend not in ALLOWED_BACKENDS:
            raise ValueError('backend has to be one of [%s]' % ','.join(ALLOWED_BACKENDS))
        elif backend not in AVAILABLE_BACKENDS:
            raise ValueError('Seems like %s is not installed' % backend)
        else:
            hydrobox.__plot_backend__ = backend
    else:
        raise AttributeError('backend has to be None or a string.')


def plot_function_loader(caller_name, backend=None):
    """
    Helper function 

    This function can be used to load plotting functions
    in case they follow the naming specification
    """
    # load module
    module_name = 'hydrobox.plotting.%s' % caller_name
    try:
        mod_ref = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise AttributeError('%s does not have a plotting routine' % caller_name)

    # load function
    backend = plotting_backend()
    function_name = '_plot_%s' % backend

    if hasattr(mod_ref, function_name):
        function = getattr(mod_ref, function_name)
    else:
        raise AttributeError('%s has no plotting routine for %s-backend' % (caller_name, backend))

    return function

