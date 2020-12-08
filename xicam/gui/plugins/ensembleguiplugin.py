from typing import Callable

from databroker.core import BlueskyRun
from xicam.core.workspace import Ensemble
from xicam.gui.models import EnsembleModel, IntentsModel
from xicam.gui.widgets.views import DataSelectorView, StackedCanvasView
from xicam.plugins import GUIPlugin


class EnsembleGUIPlugin(GUIPlugin):
    """GUI plugin that uses the Xi-CAM 'Ensemble' architecture for data organization.

    Includes an EnsembleModel, DataSelectorView, IntentsModel, and CanvasView.

    Ensemble architecture is defined primarily by an EnsembleModel class.
    This stores data in a Qt-based tree-like model, where each ensemble
    encapsulates one or more catalogs, each of which may contain Intents
    for how to visualize the data.

    """
    def __init__(self):
        super(EnsembleGUIPlugin, self).__init__()

        self.ensemble_model = EnsembleModel()

        self.intents_model = IntentsModel()
        self.intents_model.setSourceModel(self.ensemble_model)

        self.data_selector_view = DataSelectorView()
        self.data_selector_view.setModel(self.ensemble_model)

        self.canvases_view = StackedCanvasView()
        self.canvases_view.setModel(self.intents_model)

    def appendCatalog(self, catalog: BlueskyRun, projector: Callable = None, **kwargs):
        ensemble = self.ensemble_model.active_ensemble or Ensemble()
        ensemble.append_catalog(catalog)

        # TODO: use Dylan's code here instead of default projector
        def default_projector(catalog):
            return catalog

        # FIXME: how does the mainwindow discover the appropriate projector to pass here?
        self.ensemble_model.add_ensemble(ensemble, projector or default_projector)