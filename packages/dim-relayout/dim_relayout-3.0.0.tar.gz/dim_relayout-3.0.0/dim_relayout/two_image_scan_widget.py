#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF,QVariant
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
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
from .QWidget_widget import label_widget, button_widget
from .mrc_mnc_backend import mrc_mnc
from .xbpm_widget import xbpm_widget
class save_fil(QWidget):
    def __init__(self,path):
        super().__init__()
        self.btn_save = QtWidgets.QPushButton("Path")
        self.btn_save.setFixedSize(70,70)
        self.btn_load = QtWidgets.QPushButton("Load")
        self.btn_load.setFixedSize(70,70)
        self.lineedit_save = QtWidgets.QLineEdit(path)
        self.lineedit_save.setFixedSize(250,40)
        self.lineedit_save.setReadOnly(True)
        self.hlayout = QtWidgets.QHBoxLayout()
        #self.hlayout.addWidget(self.label_save)
        self.hlayout.addWidget(self.lineedit_save)
        self.hlayout.addWidget(self.btn_save)
        #self.hlayout.addWidget(self.btn_save)
        self.setLayout(self.hlayout)
        #self.btn_load.clicked.connect(self.fil_save)
    def fil_save(self):
        options = QtWidgets.QFileDialog.Options()
        options |=  QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(None,'open file dialog','/home/ke/Downloads/IHEP/BF',options=options)
        self.lineedit_save.setText(directory)
  
class two_image_scan(QWidget):
    trigger_twoD_scan_status = pyqtSignal(str)
    trigger_twoD_My_step = pyqtSignal(str)
    
    def __init__(self,mrc,mnc):
        super().__init__()
        #self.table_motor = Table_widget()
        self.msg = None
        self.scan_paused = False
        self.plt_widget = CurvePlot()
        self.img_widget = image_show(4)
        self.xbpm_widget = xbpm_widget(6)
        self.mrc_mnc = mrc_mnc(mrc,mnc)
        self.scan_paused = False
        self.count_paused = False
        self.save_path = save_fil("/home/mamba/FS_tif")
        font = QFont('Times New Roman',15)
        self.motor_list = {'slit1': ['M1.x','M1.y','M1.z'],'slit2':['M2.x','M2.y','M2.z'],'slit3':['M3.x','M3.y','M3.z']}
        self.scan_label = QLabel("scan type:    ")
        self.scan_label.setFont(font)
        self.scan_label.setFixedSize(150,40)
       
        self.detector_image = ['D.WhiteFS','D.IntegratedFS', 'D.MonochromaticFS', 'D.HRFS1', 'D.HRFS2']
        self.detector_point = ['电离室']
        self.detector_xbpm = ['D.WhiteXBPM','D.QXBPM']
        #self.motor_label = label_widget("设备")
        #self.motor_combox = QComboBox(self)
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
        self.two_Dscan.setChecked(True)
        #self.motor_vbox = QVBoxLayout()
        #self.motor_vbox.addWidget(self.motor_label)
        #self.motor_vbox.addWidget(self.motor_combox)
        
        self.scan_type_vbox =  QHBoxLayout()
        self.scan_type_vbox.addWidget(self.scan_label)
        self.scan_type_vbox.addWidget(self.one_Dscan)
        self.scan_type_vbox.addWidget(self.two_Dscan)
        self.btn_scan_start = button_widget('Start')
        self.btn_scan_start.setFixedSize(120, 100)
        self.btn_scan_pause = button_widget('Pause')
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
        groupbox.setLayout(self.hbox)
        self.scanhbox = QHBoxLayout()
        self.scanhbox.addWidget(groupbox)
        #self.hbox.addWidget(self.one_Dscan)
        #self.hbox.addWidget(self.two_Dscan)
       
        self.M1 = M_widget(1,200,mrc,mnc)
        self.M2 = M_widget(2,200,mrc,mnc)
        self.gvbox = QVBoxLayout()
        self.gvbox.addWidget(self.M1)
        self.gvbox.addWidget(self.M2)
        self.gvbox.addLayout(self.hbtnbox)
        self.groupbox1 = QGroupBox("电机")
        self.groupbox1.setLayout(self.gvbox)
        
        self.D1 = D_widget(1,200,mrc,mnc)
        #self.motor_combox.addItems(self.motor_list.keys())
        #self.M1.motor_pv_combox.addItems(self.motor_list['slit1'])
        #self.M2.motor_pv_combox.addItems(self.motor_list['slit1'])
        #self.D1.detector_combox.addItems(self.detector_image)
        #self.D1.detector_combox.addItems(self.detector_point)
        #self.D1.detector_combox.addItems(self.detector_xbpm)
        self.group_hbox = QVBoxLayout()
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.group_hbox.addLayout(self.scanhbox)
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.group_hbox.addWidget(self.groupbox1)
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        self.group_hbox.addWidget(self.D1)
        self.group_hbox.addWidget(self.save_path)
        #self.group_hbox.addWidget(self.M2)
        #self.group_hbox = QHBoxLayout()
        #self.group_hbox.addLayout(self.vbox)
        
        
        self.group_hbox.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        #self.vbox.addWidget(self.plt_widget)
        
        #groupbox1 = QGroupBox("")
        #groupbox1.setLayout(self.group_hbox)
        self.img_hbox = QHBoxLayout()
        self.img_hbox.addLayout(self.group_hbox)
        self.img_hbox.addWidget(self.img_widget)
        #self.setLayout(twogroup)        
        self.img_hbox.setStretch(0, 1)
        self.img_hbox.setStretch(1, 4)
        self.img_hbox.setSpacing(0)
        #self.setLayout(self.img_hbox)
        self.motor_1_pv()
        self.motor_2_pv()
        self.M1.motor_combox.currentIndexChanged.connect(self.motor_1_pv)
        self.M2.motor_combox.currentIndexChanged.connect(self.motor_2_pv)
        self.M1.motor_pv_combox.currentIndexChanged.connect(self.motor_pv1_disable)
        #self.M2.motor_pv_combox.currentIndexChanged.connect(self.motor_pv2_disable)
        self.motor_pv1_disable()
        self.btn_scan_start.clicked.connect(self.scan_start)
        self.btn_scan_end.clicked.connect(self.scan_end)
        self.btn_scan_pause.clicked.connect(self.scan_pause)
        self.D1.btn_D_start.clicked.connect(lambda x: self.start_count(str('twoD')))
        self.D1.btn_D_pause.clicked.connect(self.pause_count)
        self.D1.btn_D_end.clicked.connect(self.end_count)
        #self.save_path.btn_load.clicked.connect(self.img_widget.load_plot)
    def btn_status(self,msg):
        #print("******",msg)
        if msg == 'twoD_scan_stop':
           #self.D1.btn_D_start.setEnabled(True)
           #self.D1.btn_D_pause.setEnabled(False)
           #self.D1.btn_D_end.setEnabled(False)
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        if  msg == 'twoD_scan_start':
           if self.msg == 'twoD_scan_end' or self.msg == 'twoD_scan_pause':
               self.btn_scan_start.setEnabled(True)
               self.btn_scan_end.setEnabled(False)
               self.btn_scan_pause.setEnabled(False)
           else:
               self.btn_scan_start.setEnabled(False)
               self.btn_scan_end.setEnabled(True)
               self.btn_scan_pause.setEnabled(True)
        if  msg == 'twoD_scan_resume':
           self.btn_scan_start.setEnabled(False)
           self.btn_scan_end.setEnabled(True)
           self.btn_scan_pause.setEnabled(True)
        if  msg == 'twoD_scan_end':
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        if  msg == 'twoD_scan_pause':
           self.btn_scan_start.setEnabled(True)
           self.btn_scan_end.setEnabled(False)
           self.btn_scan_pause.setEnabled(False)
        self.msg = msg



    def motor_pv_update(self):
        self.M1.update_pos_now()
        self.M1.init_item()
        self.M2.update_pos_now()
        self.M2.init_item()
    def motor_1_pv(self):
        self.M1.motor_pv_combox.clear()
        #self.M2.motor_pv_combox.clear()
        motor_now = self.M1.motor_combox.currentText()
        motor_pv = self.M1.motor_list[motor_now]
        self.M1.motor_pv_combox.addItems(motor_pv)
        self.M1.init_item()
        #self.M2.motor_pv_combox.addItems(motor_pv)
    def motor_2_pv(self):
        #self.M1.motor_pv_combox.clear()
        self.M2.motor_pv_combox.clear()
        motor_now = self.M2.motor_combox.currentText()
        motor_pv = self.M2.motor_list[motor_now]
        #self.M1.motor_pv_combox.addItems(motor_pv)
        self.M2.motor_pv_combox.addItems(motor_pv)
        self.M2.init_item()
        
    def motor_pv1_disable(self):
        self.motor_2_pv()
        if (self.M1.motor_combox.currentText() == self.M2.motor_combox.currentText()):
            motor_1 = self.M1.motor_pv_combox.currentText()
            index = self.M2.motor_pv_combox.findText(motor_1)
            if index == 0:
                self.M2.motor_pv_combox.setCurrentIndex(index+1)
            self.M2.motor_pv_combox.setItemData(index,QVariant(0),Qt.UserRole-1)
            #self.M2.motor_pv_combox.setCurrentIndex(index)

    def scan_start(self):
        M_name = {}
        M_para = {}
        if self.scan_paused:
            self.scan_resume()
        else:
            try:
               self.img_widget.clear_show()
            except:
               pass
            try:
               self.xbpm_widget.clear_show()
            except:
               pass
        #self.btn_scan_start.setEnabled(False)
        #self.btn_scan_end.setEnabled(True)
        #self.btn_scan_pause.setEnabled(True)
        D_name = self.D1.detector_combox.currentText()
        #D_exp = self.D1.detector_now_lineedit.text()
        #for i in range(2):
        M1_name = self.M1.get_M_name()    
        #M1_name = self.M1.motor_pv_combox.currentText()
        M1_start,M1_end,M1_num,D_exp = self.M1.scan_para()
        #M2_name = self.M2.motor_pv_combox.currentText()
        M2_name = self.M2.get_M_name()  
        M2_start,M2_end,M2_num = self.M2.scan_para()
        self.trigger_twoD_My_step.emit(self.M1.table_motor.item(0,2).text())
        self.mrc_mnc.twoD_scan_start(M1_name,M1_start,M1_end,M1_num,M2_name,M2_start,M2_end,M2_num,D_name,D_exp)
        self.btn_scan_start.setEnabled(False)
        self.btn_scan_end.setEnabled(True)
        #self.btn_scan_pause.setEnabled(True)

        
    def scan_end(self):
        #print("&&&&&&&&&")
        self.btn_scan_start.setEnabled(True)
        #self.btn_scan_end.setEnabled(False)
        #self.btn_scan_pause.setEnabled(False)
        self.mrc_mnc.twoD_scan_end()
        self.trigger_twoD_scan_status.emit('twoD_scan_end')
    def scan_pause(self):
        self.scan_paused = True
        #self.btn_scan_start.setEnabled(True)
        #self.btn_scan_end.setEnabled(False)
        #self.btn_scan_pause.setEnabled(False)
        self.mrc_mnc.twoD_scan_pause()
        self.trigger_twoD_scan_status.emit('twoD_scan_pause')
    def scan_resume(self):
        self.scan_paused = False
        #self.btn_scan_start.setEnabled(False)
        #self.btn_scan_end.setEnabled(True)
        #self.btn_scan_pause.setEnabled(True)
        self.mrc_mnc.twoD_scan_resume()
        self.trigger_twoD_scan_status.emit('twoD_scan_resume')

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
        if D_name in self.detector_image:
            #cmd_monitor =  "%go "+ D_name +".cam.acquire.set(%d).wait()\n" % int(1)
            #self.mrc.req_rep_base("cmd", go = "", cmd = cmd_monitor)
            #self.mrc_mnc.do_cmd(cmd_monitor)
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
    w = two_image_scan()
    w.show()
    sys.exit(app.exec_())
