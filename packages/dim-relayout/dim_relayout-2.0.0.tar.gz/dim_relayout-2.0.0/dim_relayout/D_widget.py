#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from .QWidget_widget import label_widget, button_widget
from .mrc_mnc_backend import mrc_mnc

class D_widget(QWidget):
    def __init__(self,index,value_now,mrc,mnc):
        super().__init__()
        #self.table_detector = Table_widget()
        self.mrc_mnc = mrc_mnc(mrc,mnc)
        self.detector_list_read = self.mrc_mnc.get_D_list()
        #print(self.detector_list_read)
        #self.cali_b = None
        #self.cali_k = None
        #self.math_func = math_func()
        #self.motor_list = self.math_func.read_M_list(self.motor_list_read)
        self.detector_combox = QComboBox()
        self.detector_combox.setFixedSize(120, 40)
        self.detector_combox.addItems(self.detector_list_read)
        self.detector_name = label_widget("探测器"+str(index))
        self.detector_now = label_widget("积分时间")
        self.detector_now_lineedit = QLineEdit("0.2")
        self.detector_now_lineedit.setFixedSize(120, 40)
        self.loop_n = label_widget("循环次数")
        self.loop_lineedit = QLineEdit("1")
        self.loop_lineedit.setFixedSize(120, 40)
        #self.btn_roi = button_widget('ROI')
        self.btn_D_start = button_widget('Start')
        self.btn_D_start.setFixedSize(120, 40)
        self.btn_D_pause = button_widget('Pause')
        self.btn_D_pause.setFixedSize(120, 40)
        self.btn_D_end = button_widget('Stop')
        self.btn_D_end.setFixedSize(120, 40)
        self.btn_D_cali = button_widget('calibration')
        self.btn_D_cali.setFixedSize(120, 80)
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.detector_name)
        self.vbox1.addWidget(self.detector_combox)
        self.vbox1.addWidget(self.btn_D_start)
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.detector_now)
        self.vbox2.addWidget(self.detector_now_lineedit)
        self.vbox2.addWidget(self.btn_D_pause)
        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.loop_n)
        self.vbox3.addWidget(self.loop_lineedit)
        self.vbox3.addWidget(self.btn_D_end)
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox3)
        #self.hbox.addWidget(self.btn_D_cali)
        self.vbox3 = QVBoxLayout()
        self.vbox3.addLayout(self.hbox)
        #self.vbox3.addWidget(self.table_detector)
        groupbox1 = QGroupBox("探测器")#+str(index))
        groupbox1.setLayout(self.vbox3)
        self.hhbox = QHBoxLayout()
        self.hhbox.addWidget(groupbox1)
        self.setLayout(self.hhbox)
        
        
    def start_count(self,scantype):
        #print(scantype)
        D_time = self.detector_now_lineedit.text()
        D_name = self.detector_combox.currentText()
        D_loop = self.loop_lineedit.text()
        self.mrc_mnc.D_start(D_name, D_time, D_loop, str(scantype))
    def end_count(self):
        self.mrc_mnc.D_end()
    def pause_count(self):
        self.mrc_mnc.D_pause()
    def resume_count(self):
        self.mrc_mnc.D_resume()

if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #w = MainWindow()
    #sys.exit(app.exec_())
    app=QApplication(sys.argv)
    desktop = app.desktop()
    screen_size = desktop.screenGeometry()
    width = screen_size.width()
    height = screen_size.height() 
    demo = D_widget(1,200)#MainWindow(width,height)
    demo.show()
    #app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette()))
    sys.exit(app.exec_())
