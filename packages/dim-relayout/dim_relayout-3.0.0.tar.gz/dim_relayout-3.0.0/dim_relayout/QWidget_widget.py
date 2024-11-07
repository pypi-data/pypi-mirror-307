
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
import pyqtgraph
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush, ImageView
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from collections import defaultdict
from pyqtgraph import Point, GraphicsObject
from numpy import errstate,isneginf,array





ZOOMING = 1
SELECT = 2
SELECT_POLYGON = 3
PANNING = 4

SELECT_SQUARE = 123
SELECT_POLYGON = 124

# view types
INDIVIDUAL = 0
AVERAGE = 1

# selections
SELECTNONE = 0
SELECTONE = 1
SELECTMANY = 2

MAX_INSTANCES_DRAWN = 1000
MAX_THICK_SELECTED = 10
NAN = float("nan")

# distance to the first point in pixels that finishes the polygon
SELECT_POLYGON_TOLERANCE = 10

COLORBREWER_SET1 = [(228, 26, 28), (55, 126, 184), (77, 175, 74), (152, 78, 163), (255, 127, 0),
                    (255, 255, 51), (166, 86, 40), (247, 129, 191), (153, 153, 153)]



#class imageview_widget(ImageView):
#    def __init__(self):
#        super().__init__()
#        self.normRoi.setPen('r')


#class MyROI(pyqtgraph.ROI):
class MyROI(pg.ROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for a, b in [[(0, 0), (1, 1)], [(0, 1), (1, 0)],
            [(0, 0.5), (1, 0.5)], [(0.5, 0), (0.5, 1)]]:
            self.addScaleHandle(a, b)
            self.addScaleHandle(b, a)

    def getXywh(self):
        return tuple(int(x) for x in tuple(self.pos()) + tuple(self.size()))

    def setXywh(self, xywh):
        self.setPos(*xywh[:2], finish = False)
        self.setSize(xywh[2:], finish = False)

class MyImageItem(pyqtgraph.ImageItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first = True

    def setImage(self, image = None, autoLevels = None, **kwargs):
        if autoLevels is None:
            autoLevels = self.first
        super().setImage(image, autoLevels, **kwargs)
        if image is not None:
            self.first = False

class MyImageView(pyqtgraph.GraphicsLayout):
    def __init__(self, *args, view = None, imageItem = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.doStage(view, imageItem)
        self.addItem(self.view, row = 0, col = 0)
        self.addItem(self.lut, row = 0, col = 1)

    def doStage(self, view, imageItem):
        self.view = view or pyqtgraph.PlotItem()
        self.view.setAspectLocked(True)
        self.view.invertY()
        self.image = imageItem or MyImageItem()
        self.view.addItem(self.image)
        self.lut = pyqtgraph.HistogramLUTItem()
        self.lut.setImageItem(self.image)
        self.setShift(0, 0)

    def setShift(self, x, y):
        self.shift = x, y
        self.image.setTransform(QtGui.QTransform().translate(x, y))

    def setImage(self, image, autoRange = True, **kwargs):
        self.image.setImage(image, **kwargs)
        if autoRange:
            self.view.autoRange()

class ProjectImage(MyImageView):
    def __init__(self, *args, view = None,
        imageItem = None, pen = "b", **kwargs):
        pyqtgraph.GraphicsLayout.__init__(self, *args, **kwargs)
        self.doStage(view, imageItem)
        self.addItem(self.view, row = 1, col = 1)
        self.addItem(self.hplot, row = 0, col = 1)
        self.addItem(self.vplot, row = 1, col = 0)
        self.addItem(self.lut, row = 0, col = 2, rowspan = 2, colspan = 1)
        self.vplot.invertX()
        self.vplot.invertY()
        self.hproj.setPen(pen)
        self.vproj.setPen(pen)
        for item, show in [(self.view, ["left", "top"]),
            (self.hplot, ["left"]), (self.vplot, ["top"])]:
            for axis in ["left", "right", "top", "bottom"]:
                item.showAxis(axis, axis in show)

    def doStage(self, *args, **kwargs):
        super().doStage(*args, **kwargs)
        self.hplot = pyqtgraph.PlotItem()
        self.hplot.setXLink(self.view)
        self.hproj = self.hplot.plot()
        self.vplot = pyqtgraph.PlotItem()
        self.vplot.setYLink(self.view)
        self.vproj = self.vplot.plot()
        self.hplot.setMaximumHeight(80)
        self.hplot.setMinimumHeight(24)
        self.vplot.setMaximumWidth(80)
        self.vplot.setMinimumWidth(24)

    def setImage(self, image, **kwargs):
        super().setImage(image, **kwargs)
        xs, ys = numpy.arange(image.shape[1]), numpy.arange(image.shape[0])
        self.hproj.setData(self.shift[0] + xs, image.sum(0))
        self.vproj.setData(image.sum(1), self.shift[1] + ys)

class FxBpmPlot(pyqtgraph.GraphicsView):
    def __init__(self, model, titles, parent = None, mtyps = ({}, {})):
        super().__init__(parent)
        self.timer, self.delay = QtCore.QTimer(), 100
        self.timer.setSingleShot(True)
        self.ci = AlignedLines()
        self.ci.doStage(titles)
        self.setCentralItem(self.ci)
        self.timer.timeout.connect(lambda: self.submit("bpm_idle"))
        #self.sbind(model, mtyps, ["bpm_idle"])
        #self.nbind(mtyps, ["lines"])

    def on_lines(self, lines):
        for i, line in enumerate(self.ci.lines):
            line.setData(lines[0], lines[i + 1])
        self.timer.start(self.delay)

class FxBpmImage(pyqtgraph.GraphicsView):
    def __init__(self, model, parent = None, mtyps = ({}, {})):
        super().__init__(parent)
        self.timer, self.delay = QtCore.QTimer(), 100
        self.xywh = self.xs = self.ys = self.crop = self.mode = None
        self.timer.setSingleShot(True)
        self.ci = ProjectImage()
        self.roi = MyROI((0, 0))
        self.roi.setZValue(10)
        self.ci.view.addItem(self.roi)
        self.setCentralItem(self.ci)
        self.on_roi = self.roi.setXywh
        self.ci.image.hoverEvent = self.submit_hover
        self.timer.timeout.connect(lambda: self.submit("img_idle"))
        self.roi.sigRegionChangeFinished.connect\
            (lambda: self.submit("roi", self.roi.getXywh()))
        #self.sbind(model, mtyps, ["roi", "hover", "img_idle"])
        #self.nbind(mtyps, ["mode", "crop", "img", "roi"])

    def on_mode(self, mode):
        self.mode = mode
        self.roi.setVisible(mode == "open")

    def on_crop(self, xywh):
        self.ci.setShift(*xywh[:2])
        self.wh, roi = xywh[2:], xywh2roi(xywh)
        self.crop = lambda img: roi_slice(img, roi)

    def on_img(self, img):
        self.ci.setImage(self.crop(img))
        self.timer.start(self.delay)

    def submit_hover(self, ev):
        if ev.isExit():
            return
        i, j = numpy.array(self.ci.shift) + \
            numpy.clip(ev.pos(), 0, self.wh).astype(int)
        self.submit("hover", (i, j))



class label_widget(QLabel):
    def __init__(self,txt):
        super().__init__()
        font = QFont('Times New Roman', 12)
        #font.setBold(True)
        self.setFont(font)
        self.setFixedSize(120,50)
        self.setText(txt)
        self.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
class button_widget(QPushButton):
    def __init__(self,txt):
        super().__init__()
        font = QFont('Times New Roman', 12)
        #font.setBold(True)
        self.setFont(font)
        self.setFixedSize(120,50)
        self.setText(txt)

class InteractiveViewBox(ViewBox):
    def __init__(self, graph):
        ViewBox.__init__(self, enableMenu=False)
        self.setMenuEnabled(False)
        #self.gragh = graph
        self.setMouseMode(self.PanMode)
        self.zoomstartpoint = None
        self.current_selection = None
        self.action = PANNING
        self.y_padding = 0.0
        self.x_padding = 0

        # line for marking selection
        self.selection_line = pg.PlotCurveItem()
        self.selection_line.setPen(pg.mkPen(color=QColor('black'), width=2))
        self.selection_line.setZValue(1e9)
        self.selection_line.hide()
        self.addItem(self.selection_line, ignoreBounds=True)

        # yellow marker for ending the polygon
        self.selection_poly_marker = pg.ScatterPlotItem()
        self.selection_poly_marker.setPen(pg.mkPen(color=QColor('yellow'), width=2))
        self.selection_poly_marker.setSize(SELECT_POLYGON_TOLERANCE * 2)
        self.selection_poly_marker.setBrush(None)
        self.selection_poly_marker.setZValue(1e9 + 1)
        self.selection_poly_marker.hide()
        self.selection_poly_marker.mouseClickEvent = lambda x: x  # ignore mouse clicks
        self.addItem(self.selection_poly_marker, ignoreBounds=True)

        # self.sigRangeChanged.connect(self.resized)
        # self.sigResized.connect(self.resized)
        self.tiptexts = None

    def mouseMovedEvent(self, ev):  # not a Qt event!
        if self.action == ZOOMING and self.zoomstartpoint:
            pos = self.mapFromView(self.mapSceneToView(ev))
            self.updateScaleBox(self.zoomstartpoint, pos)

    def cancel_zoom(self):
        self.setMouseMode(self.PanMode)
        self.rbScaleBox.hide()
        self.zoomstartpoint = None
        self.action = PANNING
        self.unsetCursor()

    def set_mode_panning(self):
        self.cancel_zoom()
        self.enableAutoRange()

    def set_mode_zooming(self):
        self.set_mode_panning()
        self.setMouseMode(self.RectMode)
        self.action = ZOOMING
        self.setCursor(Qt.CrossCursor)

    def enableAutoRange(self, axis=None, enable=True, x=None, y=None):
        super().enableAutoRange(axis=axis, enable=False, x=x, y=y)

    def enableAutoRangeTrue(self, axis=None, enable=True, x=None, y=None):  ##########
        super().enableAutoRange(axis=axis, enable=True, x=x, y=y)


class InteractiveViewBoxC(InteractiveViewBox):
    def wheelEvent(self, ev, axis=None):
        # separate axis handling with modifier keys
        if axis is None:
            axis = 1 if ev.modifiers() & Qt.ControlModifier else 0
        super().wheelEvent(ev, axis=axis)


        
