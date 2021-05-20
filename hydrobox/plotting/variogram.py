from skgstat.plotting import backend
from skgstat import Variogram

def __plot(variogram: Variogram, plot_type: str, **kwargs): 
    # always suppress sho
    kwargs['show'] = False
    
    # get the figure
    if plot_type == 'plot':
        fig = variogram.plot(**kwargs)
    elif plot_type == 'distance_difference':
        fig = variogram.distance_difference_plot(**kwargs)
    elif plot_type == 'location_trend':
        fig = variogram.location_trend(**kwargs)
    elif plot_type == 'scattergram':
        fig = variogram.scattergram(**kwargs)
    else:
        raise ValueError(f"Plot type '{plot_type}' not supported.")

    return fig


def _plot_matplotlib(func_args, plot_args):
    # set matplotlib backend
    backend('matplotlib')

    # get the variogram
    variogram = func_args['variogram']
    plot_type = func_args.get('plot_type', 'plot')

    return __plot(variogram, plot_type, **plot_args)


def _plot_plotly(func_args, plot_args):
    # set matplotlib backend
    backend('plotly')

    # get the variogram
    variogram = func_args['variogram']
    plot_type = func_args.get('plot_type', 'plot')

    return __plot(variogram, plot_type, **plot_args)
