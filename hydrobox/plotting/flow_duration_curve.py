"""
"""
import numpy as np
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    # TODO here a global var can indicate that importing failed
    pass
try:
    from bokeh.plotting import figure, Figure
except ModuleNotFoundError:
    # TODO here a global var can indicate that importing failed
    pass


def _plot_matplotlib(func_args, plot_args):
    # parse func-args
    non_exceeding = func_args.get('non_exceeding', False)
    log = func_args.get('log', False)
    x = func_args['x']
    y = func_args['y']

    # handle matplotlib figure
    ax = func_args.get('figure')
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    else: 
        fig = ax.get_figure()
    
    # set defaults
    plot_args.setdefault('linestyle', '-')
    plot_args.setdefault('color', 'b')

    # plot
    ax.plot(x, y, **plot_args)

    ax.set_xlabel('discharge [m3/s]')
    ax.set_ylabel('%sexceeding prob.' % ('non-' if non_exceeding else ''))

    # log, log scale
    if log:
        ax.loglog()
    else:
        ax.set_ylim((-0.05, 1.1))
        ax.set_xlim(np.nanmin(x) * 0.98, np.nanmax(x) * 1.02)
    ax.set_title('%sFDC' % ('loglog ' if log else ''))
    ax.grid(which='both' if log else 'major')

    return fig        

def _plot_bokeh(func_args, plot_args):
   # parse func-args
    non_exceeding = func_args.get('non_exceeding', False)
    log = func_args.get('log', False)
    x = func_args['x']
    y = func_args['y']

    # plotting args
    plot_args.setdefault('line_color', 'navy')
    plot_args.setdefault('line_width', 3)

    fig = func_args.get('figure')
    if fig is None:
        # some of the plot_args should go into figure
        args = dict()

        for k,v in plot_args.items():
            if hasattr(Figure, k):
                args[k] = v
                del plot_args[k]
        
        # handle log-log
        if log:
            args.setdefault('x_axis_type', 'log')        
            args.setdefault('y_axis_type', 'log')
        else:
            args.setdefault('x_range', (-0.05, 1.1))
            args.setdefault('y_range', (np.nanmin(x) * 0.98, np.nanmax(x) * 1.02))
        args.setdefault('title', 'Flow duration curve')
        
        fig = figure(**args)

    # plot
    fig.line(x, y, **plot_args)

    fig.xaxis.axis_label = 'discharge [m3/s]' 
    fig.yaxis.axis_label = '%sexceeding prob.' % ('non-' if non_exceeding else '')

    return fig 

