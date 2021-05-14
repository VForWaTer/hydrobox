try:
    import matplotlib.pyplot as plt
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
