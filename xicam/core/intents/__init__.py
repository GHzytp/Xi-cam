from typing import Union
import numpy as np
import xarray
import dask.array


class Intent:
    def __init__(self, name=""):
        self._name = name
        self.match_key = None

    @property
    def name(self):
        return self._name


class ImageIntent(Intent):
    # TODO: register as entrypoint
    canvas = "image_canvas"

    def __init__(self, image, *args, **kwargs):
        super(ImageIntent, self).__init__(*args, **kwargs)
        self.image = image


class PlotIntent(Intent):
    # TODO: better labeling
    # canvas = {"qt": "plot_canvas"}
    canvas = "plot_canvas"

    def __init__(self, x: Union[np.ndarray, xarray.Dataset, dask.array.array],
                 y: Union[np.ndarray, xarray.Dataset, dask.array.array],
                 labels,
                 *args,
                 **kwargs):
        super(PlotIntent, self).__init__(*args, **kwargs)
        self.labels = labels
        self.x = x
        self.y = y
        self.match_key = hash(frozenset(self.labels.items()))

    @property
    def name(self):
        y_name = self.labels.get("left", "")
        x_name = self.labels.get("bottom", "")
        return x_name + ", " + y_name