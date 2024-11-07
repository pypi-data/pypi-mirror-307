
#!/usr/bin/python3
import configparser
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from collections import defaultdict
from pyqtgraph import Point, GraphicsObject
from numpy import errstate,isneginf,array
from qt_material import apply_stylesheet
#import qdarkstyle
#from qdarkstyle.light.palette import LightPalette
from .D_widget import D_widget
from .M_widget import M_widget
from .CurvePlot_widget import CurvePlot
from .imageshow_widget import image_show
from .xbpm_widget import xbpm_widget
from .QWidget_widget import label_widget, button_widget
from .one_image_scan_widget import one_image_scan
from .two_image_scan_widget import two_image_scan
from .thread_scan import Mythread_SCAN
from .mrc_mnc_backend import mrc_mnc        

#from dim_relayout import dim_relayout
sys.setrecursionlimit(10000)




class dim_relayout(QWidget):
    def __init__(self, parent=None):
        super(dim_relayout,self).__init__(parent)
        #super(MainWindow, self).__init__(parent)
    def detector_one_widget_cor(self):
        detector_now = self.oneDscan.D1.detector_combox.currentText()
        self.detector_one_widget(detector_now)
        self.trigger_one_connect()
    def detector_two_widget_cor(self):
        detector_now = self.twoDscan.D1.detector_combox.currentText()
        self.detector_two_widget(detector_now)
        self.trigger_two_connect()
        #index_now = self.twoDscan.D1.detector_combox.currentIndex()       
        #self.oneDscan.D1.detector_combox.setCurrentIndex(index_now)
    def detector_one_widget_ini(self):
        self.detector_now = 'D.WhiteFS'
    def detector_two_widget_ini(self):
        self.detector_now = 'D.WhiteFS'
        
    def detector_one_widget(self, detector_now):   
        #detector_now = self.oneDscan.D1.detector_combox.currentText()
        if self.detector_now in self.oneDscan.detector_point:
           self.oneDscan.plt_widget.deleteLater()
        elif self.detector_now in self.oneDscan.detector_xbpm:
           self.oneDscan.xbpm_widget.deleteLater()
        elif self.detector_now in self.oneDscan.detector_image:
           self.oneDscan.img_widget.deleteLater()

        if detector_now in self.oneDscan.detector_point:
           self.oneDscan.plt_widget = CurvePlot()
           self.oneDscan.img_hbox.addWidget(self.oneDscan.plt_widget,4)
        elif detector_now in self.oneDscan.detector_xbpm:
           self.oneDscan.xbpm_widget = xbpm_widget(6)
           self.oneDscan.img_hbox.addWidget(self.oneDscan.xbpm_widget,4)
           self.oneDscan.D_cali.clicked.connect(self.oneDscan.xbpm_widget.xbpm_cali)
           self.oneDscan.xbpm_widget.trigger_xbpm_k_b.connect(self.update_k_b)
           self.oneDscan.xbpm_widget.init_k_b(self.k_up,self.b_up,self.k_left,self.b_left)
        elif detector_now in self.oneDscan.detector_image:
           self.oneDscan.img_widget = image_show(4)
           self.oneDscan.img_hbox.addWidget(self.oneDscan.img_widget,4)
        self.detector_now = detector_now
        self.show()

    def detector_two_widget(self, detector_now):   
        #detector_now = self.twoDscan.D1.detector_combox.currentText()
        if self.detector_now in self.twoDscan.detector_point:
           self.twoDscan.plt_widget.deleteLater()
        elif self.detector_now in self.twoDscan.detector_xbpm:
           self.twoDscan.xbpm_widget.deleteLater()
        elif self.detector_now in self.twoDscan.detector_image:
           self.twoDscan.img_widget.deleteLater()

        if detector_now in self.twoDscan.detector_point:
           self.twoDscan.plt_widget = CurvePlot()
           self.twoDscan.img_hbox.addWidget(self.twoDscan.plt_widget,4)
        elif detector_now in self.twoDscan.detector_xbpm:
           self.twoDscan.xbpm_widget = xbpm_widget(6)
           self.twoDscan.img_hbox.addWidget(self.twoDscan.xbpm_widget,4)
           self.twoDscan.xbpm_widget.init_k_b(self.k_up,self.b_up,self.k_left,self.b_left)
        elif detector_now in self.twoDscan.detector_image:
           self.twoDscan.img_widget = image_show(4)
           self.twoDscan.img_hbox.addWidget(self.twoDscan.img_widget,4)
        self.detector_now = detector_now
        self.show()
if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #w = MainWindow()
    #sys.exit(app.exec_())
    app=QApplication(sys.argv)
    desktop = app.desktop()
    screen_size = desktop.screenGeometry()
    width = screen_size.width()
    height = screen_size.height() 
    demo = MainWindow(width,height)
    demo.show()
    #app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette()))
    sys.exit(app.exec_())
