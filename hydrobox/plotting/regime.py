"""
"""
import numpy as np
import colorcet as cc
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

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def _plot_matplotlib(func_args, plot_args):
    # get the df with data
    df = func_args['df']

    # load the correct cmap
    cm = getattr(cc.cm, func_args['cmap'])

    # handle matplotlib figure
    ax = func_args.get('figure')
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    else: 
        fig = ax.get_figure()

    # set plot defaults
    plot_args.setdefault('lw', 3)
    plot_args.setdefault('linestyle', '-')


    # check if there are quantiles
    if len(df.columns) > 1:
        # build the colormap
        n = int((len(df.columns) - 1) / 2)
        cmap = [cm(1. * _ / n) for _ in range(n)]
        cmap = np.concatenate((cmap, cmap[::-1]))

        # plot
        for i in range(len(df.columns) - 2, 1, -1):
            ax.fill_between(df.index, df.iloc[:, i], df.iloc[:, i - 1],
                            interpolate=True, color=cmap[i - 1])

    # plot the main aggregate
    if 'color' not in plot_args.keys():
        plot_args['color'] = cm(0.0)
    ax.plot(df.index, df.iloc[:, 0], **plot_args)
    ax.set_xlim(0, 12)
    plt.xticks(df.index, MONTHS, rotation=45)

    return fig


def _plot_bokeh(func_args, plot_args):
    # get the df with data
    df = func_args['df']

    # load the correct cmap
    cm = getattr(cc, func_args['cmap'])

    # get figure
    fig = func_args.get('figure')

    if fig is None:
        # some of the plot_args should go into figure
        args = dict()

        for k,v in plot_args.items():
            if hasattr(Figure, k):
                args[k] = v
                del plot_args[k]
        
        # set some defaults
        args.setdefault('title', 'Hydrological Regime')

        fig = figure(**args)

    # plot the percentiles at first
    if len(df.columns) > 1:
        n = int((len(df.columns) - 1) / 2)
        cmap = [cm[_] for _ in range(0, len(cm), int(len(cm) / n))]
        cmap = np.concatenate((cmap, cmap[::-1]))

        # plot
        for i in range(len(df.columns) - 2, 1, -1):
            fig.varea(
                x=df.index, y1=df.iloc[:, i], y2=df.iloc[:, i - 1],
                fill_color=cmap[i-1], fill_alpha=0.9
            )
    
    # plot the main regime
    if 'color' not in plot_args.keys():
        plot_args['color'] = cm[n]

    fig.line(df.index, df.iloc[:,0], **plot_args)

    # set the axis labels
    fig.xaxis.major_label_orientation = 45
    fig.xaxis.major_label_overrides = {i:m for i,m in enumerate(MONTHS)}

    return fig