try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    pass

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ModuleNotFoundError:
    pass


def _plot_matplotlib(func_args, plot_args):
    # build the figure
    fig, axes = plt.subplots(1, 2, figsize=plot_args.get('figsize', (12, 6)))

    # data can be one or two dimensional
    field = func_args['field']
    sigma = func_args['sigma']
    variogram = func_args['variogram']

    if field.ndim == 1:
        # plot the lines
        axes[0].plot(field)
        axes[1].plot(sigma)
        
    else:
        # plot the im
        m1 = axes[0].imshow(field, origin='lower', cmap=plot_args.get('cmap', 'terrain'))
        m2 = axes[1].imshow(sigma, origin='lower', cmap=plot_args.get('sigma_cmap', 'hot'))
        plt.colorbar(m1, ax=axes[0])
        plt.colorbar(m2, ax=axes[1])

    # label
    axes[0].set_title('Kriging Grid')
    axes[1].set_title('Kriging Error')
    plt.tight_layout()

    return fig


def _plot_plotly(func_args, plot_args):

    # get the data
    field = func_args['field']
    sigma = func_args['sigma']
    variogram = func_args['variogram']

    if  field.ndim == 1:
        fig = go.Figure()

        # build only one figure with error bars
        fig.add_trace(
            go.Scatter(
                x=range(field.flatten().size), 
                y=field.flatten(),
                mode='lines+markers',
                marker=dict(
                    size=5
                ),
                error_y=dict(
                    type='data',
                    array=sigma.flatten(),
                    visible=True
                )
            )
        )
        # return the figure
        return fig

    # if this point is reached, it's a 2D field
    if plot_args.get('surface', False):
        fig = make_subplots(1, 2, specs=[[{'type': 'surface'}, {'type': 'surface'}]])
        Trace = go.Surface
    else:
        fig = make_subplots(1, 2)    
        Trace = go.Heatmap

    # add the field
    fig.add_trace(
        Trace(z=field, colorscale=plot_args.get('colorscale', 'Earth_r')),
        1, 1
    )

    # add sigma
    fig.add_trace(
        Trace(z=sigma, colorscale=plot_args.get('sigma_colorscale', 'thermal')),
        1, 2
    )

    return fig
