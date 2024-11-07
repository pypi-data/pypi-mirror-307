#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
import time
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from collections import defaultdict
from pyqtgraph import Point, GraphicsObject
from numpy import errstate,isneginf,array
from qt_material import apply_stylesheet
import qdarkstyle
from qdarkstyle.light.palette import LightPalette
from .D_widget import D_widget
from .M_widget import M_widget
from .CurvePlot_widget import CurvePlot
from .imageshow_widget import image_show
from .xbpm_widget import xbpm_widget
from .QWidget_widget import label_widget, button_widget
from .mrc_mnc_backend import mrc_mnc
#sys.setrecursionlimit(2000)
class save_fil(QWidget):
    update_path_signal = pyqtSignal(object)
   
    def __init__(self,path):
        super().__init__()
        self.btn_save = QtWidgets.QPushButton("Save")
        self.btn_save.setFixedSize(70,70)
        self.lineedit_save = QtWidgets.QLineEdit(path)
        self.lineedit_save.setFixedSize(250,70)
        #self.lineedit_name = QtWidgets.QLineEdit(path)
        #self.lineedit_name.setFixedSize(150,70)
        #self.lineedit_save.setReadOnly(True)
        self.lineedit_save.setEnabled(False)
        self.hlayout = QtWidgets.QHBoxLayout()
        #self.hlayout.addWidget(self.label_save)
        self.hlayout.addWidget(self.lineedit_save)
        #self.hlayout.addWidget(self.lineedit_name)
        self.hlayout.addWidget(self.btn_save)
        self.setLayout(self.hlayout)
        self.btn_save.clicked.connect(self.fil_save)
    def fil_save(self):
        options = QtWidgets.QFileDialog.Options()
        options |=  QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(None,'open file dialog','/home/mamba/FS_tif',options=options)
        self.lineedit_save.setText(directory)
        self.update_path_signal.emit(directory)

class one_image_scan(QWidget):
    trigger_oneD_scan_status = pyqtSignal(str)
    #trigger_twoD_scan_status = pyqtSignal(str) 
    def __init__(self,mrc,mnc):
        super().__init__()
        #self.table_motor = Table_widget()
        self.msg = None
        self.plt_widget = CurvePlot()
        self.img_widget = image_show(4)
        self.xbpm_widget = xbpm_widget(6)
        self.mrc_mnc = mrc_mnc(mrc,mnc)
        self.scan_paused = False
        self.count_paused = False
        self.save_path = save_fil("/home/mamba/FS_tif")
        font = QFont('Times New Roman',15)
        #self.motor_list = {'slit1': ['M1.x','M1.y','M1.z'],'slit2':['M2.x','M2.y','M2.z'],'slit3':['M3.x','M3.y','M3.z']}
        self.scan_label = QLabel("scan type:    ")
        self.scan_label.setFont(font)
        self.scan_label.setFixedSize(150,40)
        #self.detector_image = ['荧光靶','camera']
        #self.detector_point = ['电离室']
        #self.detector_xbpm = ['XBPM']
        self.detector_image = ['D.WhiteFS','D.IntegratedFS', 'D.MonochromaticFS', 'D.HRFS1', 'D.HRFS2']
        self.detector_point = ['电离室']
        self.detector_xbpm = ['D.WhiteXBPM','D.QXBPM']
        
        #self.motor_label = label_widget("设备")
        #self.motor_combox = QComboBox()
        #self.detector_combox = QComboBox(self)
        #self.motor_pv_combox = QComboBox(self)
        #self.motor_combox.setFixedSize(100, 40)
        #self.motor_pv_combox.setFixedSize(100, 40)
        #self.detector_combox.setFixedSize(100, 40)
        self.one_Dscan = QRadioButton("1D scan")
        self.two_Dscan = QRadioButton("2D scan")
        self.one_Dscan.setFixedSize(150,40)
        self.one_Dscan.setFont(font)
        self.two_Dscan.setFixedSize(150,40)
        self.two_Dscan.setFont(font)
        self.one_Dscan.setChecked(True)
        #self.motor_vbox = QVBoxLayout()
        #self.motor_vbox.addWidget(self.motor_label)
        #self.motor_vbox.addWidget(self.motor_combox)
        self.scan_type_vbox =  QHBoxLayout()
        self.scan_type_vbox.addWidget(self.scan_label)
        self.scan_type_vbox.addWidget(self.one_Dscan)
        self.scan_type_vbox.addWidget(self.two_Dscan)
        self.btn_scan_start = button_widget('Start scan')
        self.btn_scan_start.setFixedSize(120, 100)
        self.btn_scan_pause = button_widget('Pause scan')
        self.btn_scan_pause.setFixedSize(120, 100)
        self.btn_scan_end = button_widget('End')
        self.btn_scan_end.setFixedSize(120, 100)
        self.hbtnbox = QHBoxLayout()
        self.hbtnbox.addWidget(self.btn_scan_start)
        self.hbtnbox.addWidget(self.btn_scan_pause)
        self.hbtnbox.addWidget(self.btn_scan_end)
        
        self.hbox = QHBoxLayout()
        #self.hbox.addLayout(self.motor_vbox)
        self.hbox.addLayout(self.scan_type_vbox)
        groupbox = QGroupBox("扫描类型")
        font = QFont('Song', 20)
        #groupbox.setFont(font)
        groupbox.setLayout(self.hbox)
        self.scanhbox = QVBoxLayout()
        self.scanhbox.addWidget(groupbox)

        self.M1 = M_widget(1,200,mrc,mnc)
        self.gvbox = QVBoxLayout()
        self.gvbox.addWidget(self.M1)
        self.gvbox.addLayout(self.hbtnbox)
        self.groupbox1 = QGroupBox("电机")
        #self.groupbox1.setFont(font)
        self.groupbox1.setStyleSheet("""QGroupBox::title{font-size:70px;}""")
        self.groupbox1.setLayout(self.gvbox)
        self.D1 = D_widget(1,200,mrc,mnc)

        self.D_cali = button_widget('Calibration')
        self.D_cali.setFixedSize(120, 100)
        self.DBOX = QHBoxLayout()
        self.DBOX.addWidget(self.D1,5)
        self.DBOX.addWidget(self.D_cali,1)   
        #self.motor_combox.addItems(self.motor_list.keys())
        #self.M1.motor_pv_combox.addItems(self.motor_list['slit1'])
        #self.D1.detector_combox.addItems(self.detector_image)
        #self.D1.detector_combox.addItems(self.detector_point)
        #self.D1.detector_combox.addItems(self.detector_xbpm)
        self.group_hbox = QVBoxLayout()
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.group_hbox.addLayout(self.scanhbox)
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.group_hbox.addWidget(self.groupbox1)
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        #self.group_hbox.addWidget(self.D1)       
        self.group_hbox.addLayout(self.DBOX) 
        self.group_hbox.addWidget(self.save_path)
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.img_hbox = QHBoxLayout()        
        self.img_hbox.addLayout(self.group_hbox,1)
        self.img_hbox.addWidget(self.img_widget,4)
        self.motor_pv()
        self.M1.motor_combox.currentIndexChanged.connect(self.motor_pv)
        self.M1.motor_pv_combox.currentIndexChanged.connect(self.motor_pv_update)
        self.D1.btn_D_start.clicked.connect(lambda x: self.start_count(str('oneD')))
        self.D1.btn_D_pause.clicked.connect(self.pause_count)
        self.D1.btn_D_end.clicked.connect(self.end_count)
        self.btn_scan_start.clicked.connect(self.scan_start)
        self.btn_scan_end.clicked.connect(self.scan_end)
        self.btn_scan_pause.clicked.connect(self.scan_pause)
      
    def btn_status(self,msg):
        #print("******",msg)
        if msg == 'oneD_scan_stop':
           #self.D1.btn_D_start.setEnabled(True)
           #self.D1.btn_D_pause.setEnabled(False)
           #self.D1.btn_D_end.setEnabled(False)
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        if  msg == 'oneD_scan_start':
           if self.msg == 'oneD_scan_end' or self.msg == 'oneD_scan_pause':
               self.btn_scan_start.setEnabled(True)
               self.btn_scan_end.setEnabled(False)
               self.btn_scan_pause.setEnabled(False)
           else:
               self.btn_scan_start.setEnabled(False)
               self.btn_scan_end.setEnabled(True)
               self.btn_scan_pause.setEnabled(True)
        if  msg == 'oneD_scan_resume':
           self.btn_scan_start.setEnabled(False)
           self.btn_scan_end.setEnabled(True)
           self.btn_scan_pause.setEnabled(True)
        if  msg == 'oneD_scan_end':
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        if  msg == 'oneD_scan_pause':
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        self.msg = msg
    def motor_pv_update(self):
        self.M1.update_pos_now()
        self.M1.init_item()
    def motor_pv(self):
        self.M1.motor_pv_combox.clear()
        motor_now = self.M1.motor_combox.currentText()
        motor_pv = self.M1.motor_list[motor_now]
        self.M1.motor_pv_combox.addItems(motor_pv)
        self.M1.init_item()
        #self.motor_pv_update()
    def scan_start(self):
        if self.scan_paused:
            self.scan_resume()
        else:
            try:
               self.img_widget.clear_show()
            except:
               pass
            try:
               self.xbpm_widget.clear_show()
               self.add_cal_inf()
            except:
               pass
            D_name = self.D1.detector_combox.currentText()
            #D_exp = self.D1.detector_now_lineedit.text()
            #exp_now = self.M1.motor_combox.currentText()
            #M_pv_name = self.M1.motor_pv_combox.currentText()
            M_name = self.M1.get_M_name()
            self.M_current = self.M1.motor_now_lineedit.text()
            M_start,M_end,M_num,D_exp = self.M1.scan_para()
            self.mrc_mnc.oneD_scan_start(M_name,M_start,M_end,M_num,D_name,D_exp)
            self.btn_scan_start.setEnabled(False)
            self.btn_scan_end.setEnabled(True)
    def add_cal_inf(self):
        self.xbpm_widget.plot_items[4].plot.addItem(self.xbpm_widget.infs[0])
        self.xbpm_widget.plot_items[4].plot.addItem(self.xbpm_widget.infs[1])
        self.xbpm_widget.plot_items[5].plot.addItem(self.xbpm_widget.infs[2])
        self.xbpm_widget.plot_items[5].plot.addItem(self.xbpm_widget.infs[3])    
    def scan_end(self):
        #print("&&&&&&&&&")
        self.btn_scan_start.setEnabled(True)
        #self.btn_scan_end.setEnabled(False)
        #self.btn_scan_pause.setEnabled(False)
        self.mrc_mnc.oneD_scan_end()
        self.trigger_oneD_scan_status.emit('oneD_scan_end')
        #time.sleep(1)
        #self.trigger_oneD_scan_status.emit('oneD_scan_end')
        #self.D1.btn_D_start.setEnabled(True)
        #self.D1.btn_D_pause.setEnabled(False)
        #self.D1.btn_D_end.setEnabled(False)
    def scan_pause(self):
        self.scan_paused = True
        #self.btn_scan_start.setEnabled(True)
        #self.btn_scan_end.setEnabled(False)
        #self.btn_scan_pause.setEnabled(False)
        self.mrc_mnc.oneD_scan_pause()
        self.trigger_oneD_scan_status.emit('oneD_scan_pause')
    def scan_resume(self):
        self.scan_paused = False
        #self.btn_scan_start.setEnabled(False)
        #self.btn_scan_end.setEnabled(True)
        #self.btn_scan_pause.setEnabled(True)
        self.mrc_mnc.oneD_scan_resume()
        self.trigger_oneD_scan_status.emit('oneD_scan_resume')

    def start_count(self,scantype):
        #print(scantype)
        if self.count_paused:
            self.resume_count()
        else:
            try:
               self.img_widget.clear_show()
            except:
               pass
            try:
               self.xbpm_widget.clear_show()
            except:
               pass
            #self.img_widget.clear_show()
            #self.xbpm_widget.clear_show()
            D_time = self.D1.detector_now_lineedit.text()
            D_name = self.D1.detector_combox.currentText()
            D_loop = self.D1.loop_lineedit.text()
            self.mrc_mnc.D_start(D_name, D_time, D_loop, str(scantype))
    def end_count(self):
        self.mrc_mnc.D_end()
        D_name = self.D1.detector_combox.currentText()
        print(D_name)
        if D_name in self.detector_image:
            self.mrc_mnc.D_image_cam(D_name)
        else:
            pass
        #self.D1.btn_D_start.setEnabled(True)
        #self.D1.btn_D_pause.setEnabled(False)
        #self.D1.btn_D_end.setEnabled(False)
        self.btn_scan_start.setEnabled(True)
        #self.btn_scan_end.setEnabled(False)
        #self.btn_scan_pause.setEnabled(False)
    def pause_count(self):
        self.count_paused = True
        self.mrc_mnc.D_pause()
        #self.D1.btn_D_start.setEnabled(True)
        #self.D1.btn_D_pause.setEnabled(False)
        #self.D1.btn_D_end.setEnabled(False)

    def resume_count(self):
        self.count_paused = False
        self.mrc_mnc.D_resume()
        #self.D1.btn_D_start.setEnabled(True)
        #self.D1.btn_D_pause.setEnabled(False)
        #self.D1.btn_D_end.setEnabled(False)

 
if __name__ == '__main__':        
    app = QApplication(sys.argv)
    w = one_image_scan()
    w.show()
    sys.exit(app.exec_())
