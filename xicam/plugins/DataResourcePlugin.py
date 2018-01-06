from yapsy.IPlugin import IPlugin

viewTypes = ["ListView", "TreeView", ""]


class DataResourcePlugin(IPlugin):
    def __init__(self, flags: dict = None, **config):
        """
        Config keys should follow RFC 3986 URI format:
            scheme:[//[user[:password]@]host[:port]][/path][?query][#fragment]

        Should provide the abstract methods required of QAbstractItemModel. While this plugin does not depend on Qt, it
        mimics the same functionality, and so can easily be wrapped in a QAbstractItemModel for GUI views. A parent
        model assigns itself to self.model
        """
        super(DataResourcePlugin, self).__init__()
        self.model = None
        self.config = config
        self.flags = flags if flags else {'isFlat': True, 'canPush': False}

    def pushData(self, *args, **kwargs):
        raise NotImplementedError

    def dataChanged(self, topleft=None, bottomright=None):
        if self.model:
            self.model.dataChanged.emit(topleft, bottomright)

    def columnCount(self, index=None):
        raise NotImplementedError

    def rowCount(self, index=None):
        raise NotImplementedError

    def data(self, index, role):
        raise NotImplementedError

    def headerData(self, column, orientation, role):
        raise NotImplementedError

    def index(self, row, column, parent):
        raise NotImplementedError

    def parent(self, index):
        raise NotImplementedError

    @property
    def host(self): return self.config['host']

    @property
    def path(self): return self.config['path']

    # TODO: convenience properties for each config


try:
    from qtpy.QtCore import *


    class DataSourceItemModel(QAbstractItemModel):
        def __init__(self, dataresource: DataResourcePlugin):
            super(DataSourceItemModel, self).__init__()
            self.dataresource = dataresource
            self.dataresource.model = self
            self.columnCount = dataresource.columnCount
            self.rowCount = dataresource.rowCount
            self.data = dataresource.data
            self.headerData = dataresource.headerData


    class DataSourceListModel(QAbstractListModel, DataSourceItemModel):
        def __init__(self, dataresource: DataResourcePlugin):
            super(DataSourceListModel, self).__init__(dataresource)
except ImportError:
    # TODO: how should this be handled?
    pass
