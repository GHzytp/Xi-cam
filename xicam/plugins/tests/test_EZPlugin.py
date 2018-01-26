from xicam.plugins import EZPlugin
from xicam.gui.static import path
from xicam.core.data import NonDBHeader


def test_EZPlugin():
    def runtest():
        import numpy as np

        img = np.random.random((100, 100, 100))
        EZTest.instance.setImage(img)

        hist = np.histogram(img, 100)
        EZTest.instance.plot(hist[1][:-1], hist[0])

    def appendheadertest(header: NonDBHeader):
        img = header.meta_array(list(header.fields())[0])
        EZTest.instance.setImage(img)

    EZTest = EZPlugin(name='EZTest',
                      toolbuttons=[(str(path('icons/calibrate.png')), runtest)],
                      parameters=[{'name': 'Test', 'value': 10, 'type': 'int'},
                                  {'name': 'Fooo', 'value': True, 'type': 'bool'}],
                      appendheadertest=appendheadertest)