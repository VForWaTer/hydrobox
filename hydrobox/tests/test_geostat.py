from hydrobox import data
import hydrobox
import plotly.graph_objects as go
import skgstat as skg


def test_variogram():
    """Test the return types"""
    # get data
    df = data.pancake()
    hydrobox.plotting_backend('plotly')

    for t, type_ in zip(('object', 'describe', 'plot'), (skg.Variogram, dict, go.Figure)):
        vario = hydrobox.geostat.variogram(
            df[['x', 'y']].values,
            df.z.values,
            return_type=t
        )

        assert isinstance(vario, type_)
