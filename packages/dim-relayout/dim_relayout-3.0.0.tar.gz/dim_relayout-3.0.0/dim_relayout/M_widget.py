from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar, QMessageBox
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF, QTimer
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
from .QWidget_widget import label_widget, button_widget
from .mrc_mnc_backend import mrc_mnc
import math
from .math_func import math_func
import datetime
import numpy as np
class Table_widget(QTableWidget):
    def __init__(self):
        super().__init__()
        #self = QTableWidget(self)
        #self.setFixedSize(350,120)
        self.setSelectionBehavior(1)
        font = QFont('Times New Roman', 12)
        font.setBold(True)
        self.setColumnCount(5)
        self.setRowCount(2)
        self.setItem(0,0,QTableWidgetItem(None))
        self.setItem(0,1,QTableWidgetItem(None))
        self.setItem(0,2,QTableWidgetItem(str(0.1)))
        self.setItem(0,3,QTableWidgetItem(str(0.1)))
        self.setItem(0,4,QTableWidgetItem("绝对位置"))
        self.setItem(1,0,QTableWidgetItem(str(-1.0)))
        self.setItem(1,1,QTableWidgetItem(str(1.0)))
        self.setItem(1,2,QTableWidgetItem(str(0.1)))
        self.setItem(1,3,QTableWidgetItem(str(0.1)))
        self.setItem(1,4,QTableWidgetItem("相对位置"))
        self.headers = ['Start','End','Step','Time(s)','']
        self.setHorizontalHeaderLabels(self.headers)
        self.horizontalHeader().setFont(font)  # 设置表头字体
        self.horizontalHeader().setStyleSheet('QHeaderView::section{background:gray}')
        self.horizontalHeader().setFixedHeight(30)
        self.setFixedHeight(90)
        #self.addItem([])
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #self.verticalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

class M_widget(QWidget):
    def __init__(self,index,value_now,mrc,mnc):
        super().__init__()
        self.mrc_mnc = mrc_mnc(mrc,mnc)
        self.motor_list_read = self.mrc_mnc.get_M_list()
        self.math_func = math_func()
        self.motor_list = self.math_func.read_M_list(self.motor_list_read)
        self.table_motor = Table_widget()
        self.motor_pv_combox = QComboBox(self)
        self.motor_pv_combox.setFixedSize(100, 40)
        #self.motor_list = M_name
        self.motor_label = label_widget("设备")
        self.motor_combox = QComboBox(self)
        self.motor_combox.setFixedSize(100, 40)
        self.motor_combox.addItems(self.motor_list.keys())
        ele_motor = list(self.motor_list.keys())
        ele_motor_pv = self.motor_list[ele_motor[0]]
        self.motor_pv_combox.addItem(ele_motor_pv[0])
        self.motor_name = label_widget("Motor_"+str(index))
        self.motor_now = label_widget("current")
        self.motor_now_lineedit = QLineEdit()
        self.motor_now_lineedit.setFixedSize(170, 40)
        self.motor_target = label_widget("target")
        self.motor_target_lineedit = QLineEdit()
        self.motor_target_lineedit.setFixedSize(100, 40)

        self.vbox0 = QVBoxLayout()
        self.vbox0.addWidget(self.motor_label)
        self.vbox0.addWidget(self.motor_combox)
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.motor_name)
        self.vbox1.addWidget(self.motor_pv_combox)
         
        self.vbox22 = QVBoxLayout()
        self.vbox22.addWidget(self.motor_target)
        self.vbox22.addWidget(self.motor_target_lineedit)
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.motor_now)
        self.vbox2.addWidget(self.motor_now_lineedit)
        self.btn_M_move = button_widget('Move')
        self.btn_M_move.setFixedSize(120, 40)
        self.btn_M_stop = button_widget('Stop')
        self.btn_M_stop.setFixedSize(120, 40)
        self.vbox23 = QVBoxLayout()
        self.vbox23.addWidget(self.btn_M_move)
        self.vbox23.addWidget(self.btn_M_stop)
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox0)
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox22)
        self.hbox.addLayout(self.vbox23)
        self.vbox3 = QVBoxLayout()
        self.vbox3.addLayout(self.hbox)
        self.vbox3.addWidget(self.table_motor)
        self.vbox3.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding))
        groupbox1 = QGroupBox("")
        groupbox1.setLayout(self.vbox3)
        self.hhbox = QHBoxLayout()
        self.hhbox.addWidget(groupbox1)
        self.setLayout(self.hhbox)
        self.btn_M_move.clicked.connect(self.start_move)
        self.btn_M_stop.clicked.connect(self.stop_move)
        self.timer =  QTimer()
        self.starttime()
        self.init_item()
        self.sig_change = 1
        self.table_motor.cellChanged.connect(self.cellchange)
    def get_M_name(self):
        M_name_name = self.motor_combox.currentText()
        M_name_pv = self.motor_pv_combox.currentText()
        M_name = M_name_name+'_'+M_name_pv
        return(M_name)
    def start_move(self):
        M_pos = self.motor_target_lineedit.text()
        #M_name = self.motor_pv_combox.currentText()
        M_name = self.get_M_name()
        #M_name_name = self.motor_combox.currentText()
        #M_name_pv = self.motor_pv_combox.currentText()
        #M_name = M_name_name+'_'+M_name_pv
        pos_high,pos_low = self.mrc_mnc.limit_M_pos(M_name)
        print(pos_high,pos_low)
        if M_pos == "":
           self.messagebox = QMessageBox.critical(self,'提示','please input target',QMessageBox.Yes|QMessageBox.Yes)
        elif pos_low > float(M_pos) or pos_high < float(M_pos):
            self.messagebox = QMessageBox.critical(self,'提示','please check  target  in range ['+str(pos_low)+','+str(pos_high)+']',QMessageBox.Yes|QMessageBox.Yes)
        else:
        #D_loop = self.loop_lineedit.text()
           #self.btn_M_move.setEnabled(False)
           #self.btn_M_stop.setEnabled(True)
           #self.mrc_mnc.mrc.do_cmd("%go "+ M_name +".set(%f).wait()\n" % float(M_pos)).subscribe(self.cb)
           self.mrc_mnc.set_M(M_name, M_pos)#.subscribe(self.cb)
    def cb(self,rep):
        #self.btn_M_move.setEnabled(True)
        #self.btn_M_stop.setEnabled(False)
        self.motor_target_lineedit.clear()
    def stop_move(self):
        #M_name = self.motor_pv_combox.currentText()
        M_name = self.get_M_name()
        self.mrc_mnc.stop_M(M_name)
        #self.btn_M_move.setEnabled(True)
        #self.btn_M_stop.setEnabled(False)
    def update_pos_now(self):
        #M_name_name = self.motor_combox.currentText()
        #M_name_pv = self.motor_pv_combox.currentText()
        #M_name = M_name_name+'_'+M_name_pv
        M_name = self.get_M_name()
        #print(M_name)
        self.pos_now,self.pos_unit = self.mrc_mnc.get_M_pos(M_name)
        #print(self.pos_now,self.pos_unit)
        self.motor_now_lineedit.setText(str('%.4f'%self.pos_now) + self.pos_unit)
    def init_item(self):
        M_name = self.get_M_name()
        self.pos_now,self.pos_unit = self.mrc_mnc.get_M_pos(M_name)
        for i in range(2):
           item = self.table_motor.item(1,i)
           txt = item.text()
           text_input =  float(txt)+ float(self.pos_now)
           self.table_motor.setItem(0,i,QTableWidgetItem(str('%.2f'%text_input))) 
    def scan_para(self):
        M_start = self.table_motor.item(0,0).text()
        M_end = self.table_motor.item(0,1).text()
        M_step = self.table_motor.item(0,2).text()
        D_exp = self.table_motor.item(0,2).text()
        print(M_start,M_end,M_step)
        M_num = int(np.ceil((float(M_end)-float(M_start))/float(M_step))) + 1
        print(M_start,M_end,M_num)
        return(M_start,M_end,M_num,D_exp)
    def starttime(self):
        self.timer.start(200)
        self.timer.timeout.connect(self.update_pos_now)
    def cellchange(self,row,col):
        if self.sig_change % 2 : 
           self.item_change(row,col)
    def item_change(self,row,col):
        #print(row,col)
        self.sig_change = False
        item = self.table_motor.item(row,col)
        txt = item.text()
        #print(row,col)
        #print(txt)
        if (col == 0 or col == 1):
            if (row % 2 == 0):
              #self.energy_range_check(float(txt)+float(self.energy_abso))
              try:
                  text_input =  float(txt)- float(self.pos_now)
                  self.table_motor.setItem(row+1,col,QTableWidgetItem(str('%.2f'%text_input))) 
              except:
                  self.messagebox = QMessageBox.critical(self,'提示','please check the input', QMessageBox.Yes|QMessageBox.Yes)
              
            else:
              try:
                  text_input = float(txt)+ float(self.pos_now)
                  self.table_motor.setItem(row-1,col,QTableWidgetItem(str('%.2f'%text_input)))
              except:
                  self.messagebox = QMessageBox.critical(self,'提示','please check the input', QMessageBox.Yes|QMessageBox.Yes)
             
        if (col == 2 or col == 3):
            if (row % 2 == 0):
               self.table_motor.setItem(row+1,col,QTableWidgetItem(str('%.2f'% float(txt))))
            else:
               self.table_motor.setItem(row-1,col,QTableWidgetItem(str('%.2f'% float(txt)))) 
        self.sig_change += 1
if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #w = MainWindow()
    #sys.exit(app.exec_())
    app=QApplication(sys.argv)
    desktop = app.desktop()
    screen_size = desktop.screenGeometry()
    width = screen_size.width()
    height = screen_size.height() 
    demo = M_widget(1,200)#MainWindow(width,height)
    demo.show()
    #app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette()))
    sys.exit(app.exec_())
