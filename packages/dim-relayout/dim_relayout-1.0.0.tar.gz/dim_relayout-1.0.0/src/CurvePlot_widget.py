import sys
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from collections import defaultdict
from pyqtgraph import Point, GraphicsObject
from numpy import errstate,isneginf,array
from .QWidget_widget import InteractiveViewBoxC






class CurvePlot(QWidget):
    limits_changed = pyqtSignal()

    def __init__(self, parent=None):
        super(CurvePlot, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.plotview = pg.PlotWidget(background="w", viewBox=InteractiveViewBoxC(self))
        #self.plotview.setXRange(0,2000)
        self.plotview.getPlotItem().addLegend()
        self.plot = self.plotview.getPlotItem()
        self.plot.hideButtons()  # hide the autorange button
        self.plot.setDownsampling(auto=True, mode="peak")
        self._curves = {}
        self._current_vline = None

        self.markings = []
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot.scene().sigMouseMoved.connect(self.mouse_moved_viewhelpers)
        self.plot.scene().sigMouseMoved.connect(self.plot.vb.mouseMovedEvent)
        self.plot.setLabel('bottom', 'M')
        # interface settings
        self.markclosest = True  # mark
        self.crosshair = True

        # ----------------QToolBar---------------------------------------
        self.navbar = QToolBar()
        self.navbar.setIconSize(QSize(20, 20))
        self.navbar.setStyleSheet("font-size:15px;")
        self.navbar.addAction(QIcon('/home/mamba/mamba/mamba/frontend/icon/button_grid.png'),
                              "Show grid", self.grid_changed)
        self.navbar.addAction(QIcon('/home/mamba/mamba/mamba/frontend/icon/button_big.png'),
                              "Zoom in", self.plot.vb.set_mode_zooming)
        self.navbar.addAction(QIcon('/home/mamba/mamba/mamba/frontend/icon/button_arrow.png'),
                              "move", self.plot.vb.set_mode_panning)
        self.navbar.addAction(QIcon('/home/mamba/mamba/mamba/frontend/icon/button_fount.png'),
                              "auto", self.plot.vb.enableAutoRangeTrue)
        #self.navbar.addAction(QIcon('/home/mamba/mamba/mamba/frontend/icon/log.png'),
         #                     "log", self.set_log)

        spacer1 = QWidget()
        spacer2 = QWidget()
        #spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.navbar.addWidget(spacer1)
        self.axis_label = QLabel("")
        self.max_min_label = QLabel("")
        self.navbar.addWidget(self.axis_label)
        self.navbar.addWidget(spacer2)
        self.navbar.addWidget(self.max_min_label)
        vbox = QVBoxLayout()
        #vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.navbar)
        vbox.addWidget(self.plotview)
        #self.setLayout(vbox)
        groupbox1 = QGroupBox("")
        groupbox1.setLayout(vbox)
        twogroup = QHBoxLayout()
        twogroup.addWidget(groupbox1)
        self.setLayout(twogroup)
        # -------------------------------------------------------------------

        self.show_grid = False
        self.log = False
        self.grid_changed()

    def grid_changed(self):
        self.show_grid = not self.show_grid
        self.grid_apply()

    def set_log(self):
        self.log = not self.log
        for curve_id in self._curves:
            if self._curves[curve_id]["y"] is not None:
               self.set_values(curve_id, self._curves[curve_id]["x"], self._curves[curve_id]["y"])

    def grid_apply(self):
        self.plot.showGrid(self.show_grid, self.show_grid)

    def mouse_moved_viewhelpers(self, pos):
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.vb.mapSceneToView(pos)
            posx, posy = mousePoint.x(), mousePoint.y()
            labels = str(round(posx, 4)) + "   " + str(round(posy, 4))
            self.axis_label.setText(labels)

    def add_curve(self, curve_id, curve_name, curve_color=QColor('blue'), markers_on=False):
        pen = mkPen(curve_color, width=2)
        symbol = "o"
        symbolPen = mkPen(QColor('red'))
        symbolBrush = mkBrush(curve_color)
        # this adds the item to the plot and legend
        if markers_on:
            a = self.plot
            plot = self.plot.plot(name=curve_name, pen=pen, symbol=symbol, symbolPen=symbolPen,
                                  symbolBrush=symbolBrush, symbolSize=4)
            # a.setLabel('left', "Y Axis", units='A')
            # a.setLabel('bottom', "Y Axis", units='s')
        else:
            a = self.plot
            plot = a.plot(name=curve_name, pen=pen)

            # a.setLabel('left', "Y Axis", units='A')
            # a.setLabel('bottom', "Y Axis", units='s')
        self._curves[curve_id] = {}
        self._curves[curve_id]["plot"] = plot
        self._curves[curve_id]["x"] = None
        self._curves[curve_id]["y"] = None

    def remove_curve(self, curve_id):
        if curve_id in self._curves:
            self.plot.removeItem(self._curves[curve_id]["plot"])
            del self._curves[curve_id]
            self._update_legend()

    def _update_legend(self):
        # clear and rebuild legend (there is no remove item method for the legend...)
        self.plot.clear()
        self.plot.getPlotItem().legend.items = []
        for curve in self._curves.values():
            self.plot.addItem(curve["plot"])
        if self._current_vline:
            self.plot.addItem(self._current_vline)

    def set_values(self, curve_id, data_x, data_y):
        self._curves[curve_id]["x"] = data_x
        self._curves[curve_id]["y"] = data_y
        curve = self._curves[curve_id]["plot"]
        if self.log:
            with errstate(divide='ignore'):
                data_y = np.log10(data_y)
                data_y[isneginf(data_y)] = 0
        curve.setData(data_x, data_y)

    def vline(self, x, color):
        if self._current_vline:
            self.plot.removeItem(self._current_vline)
        self._current_vline = self.plot.addLine(x=x, pen=color)
        # self._current_vline.sigDragged.connect(self.aaa)
    
    def set_axis_name(self, x_name=None, y_name=None):
        if x_name is not None:
            self.plot.setLabel('bottom', x_name)
        if y_name is not None:
            self.plot.setLabel('left', y_name)

if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #w = MainWindow()
    #sys.exit(app.exec_())
    app=QApplication(sys.argv)
    demo = CurvePlot()
    demo.show()
    #app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette()))
    sys.exit(app.exec_())
