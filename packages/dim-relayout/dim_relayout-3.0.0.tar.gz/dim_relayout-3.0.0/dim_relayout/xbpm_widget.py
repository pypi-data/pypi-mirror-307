from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
#from faker import Factory
import random
import sys
import math
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from collections import defaultdict
from pyqtgraph import Point, GraphicsObject
from numpy import errstate,isneginf,array
from qt_material import apply_stylesheet
import qdarkstyle
import numpy as np
from .CurvePlot_widget import CurvePlot
#from imageshow_widget import image_show
from .QWidget_widget import label_widget, button_widget
import datetime

class xbpm_widget(QWidget):
    trigger_xbpm_k_b = pyqtSignal(float,float,float,float)
    def __init__(self,n):
        super().__init__()
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(imageAxisOrder='row-major')
        #screen_size = desktop.screenGeometry()
        #width = screen_size.width()
        #height = screen_size.height()
        #self.width = int(width/2)
        #self.height = int(height*0.8)
        self.y_axis = None
        self.y_axis_get = False
        self.save_path = '/home/mamba/FS_tif'
        self.color_list = [(200,0,0),(0,150,0),(0,0,200),(0,0,0)]
        self.y_axis_name = ['sum_I','I','Ia+Ib & Ic+Id','Ia+Ic & Ib+Id','Ia+Ib/(Ic+Id)','Ia+Ic/(Ib+Id)']
        self.plot_items = []
        self.infs = []
        #self.vbox_plt = QVBoxLayout()
        self.vbox_plt = QGridLayout()
        self.plotimg_item = pg.PlotItem()
        #self.plotview = pg.PlotWidget(background="w", viewBox=InteractiveViewBoxC(self))
        ##self.plotview.setXRange(0,2000)
        #self.plotview.getPlotItem().addLegend()
        #self.plot = self.plotview.getPlotItem()
        #self.plot.hideButtons()  # hide the autorange button
        #self.plot.setDownsampling(auto=True, mode="peak")
        self.n_index = n
        for i in range(math.ceil(n/2)):
            for j in range(2):
                self.plot_item = CurvePlot()
                self.plot_item.set_axis_name("M",self.y_axis_name[2*i+j])
                #self.plot_item.setFixedSize(500, 200)
                self.plot_items.append(self.plot_item)
                self.vbox_plt.addWidget(self.plot_item,i,j)
        for i in range(4):
             inf = pg.InfiniteLine(movable=True, angle=90, pen=pg.mkPen(color='#FFA500',width = 3),label='x={value:0.2f}', labelOpts={'position':0.1, 'color':'#FF0000', 'fill': (200,200,200,200), 'movable': True})
             inf.setPos([0.5*i, 0.5*i])
             self.infs.append(inf)
        self.plot_items[4].plot.addItem(self.infs[0])
        self.plot_items[4].plot.addItem(self.infs[1])
        self.plot_items[5].plot.addItem(self.infs[2])
        self.plot_items[5].plot.addItem(self.infs[3])
        #self.legend1 = self.plot_items[1].addLegend(frame=True, colCount=1, offset=(-10, 5))
        self.hbox = QHBoxLayout()
        #vbox.setContentsMargins(0, 0, 0, 0)
        #vbox.addWidget(self.navbar)
        self.hbox.addLayout(self.vbox_plt,1)
        #self.hbox.addWidget(self.image_view,1)
        
        #self.setLayout(vbox)
        groupbox1 = QGroupBox("")
        groupbox1.setLayout(self.hbox)
        twogroup = QHBoxLayout()
        twogroup.addWidget(groupbox1)
        self.setLayout(twogroup)
        #self.show()
    def update_2d_motor_detector(self,motor_y,motor_x,detector):
        self.name_detector = detector
        self.name_motor_x = motor_x
        self.name_motor_y = motor_y
        #print(self.name_motor_x,self.name_detector)
    def update_motor_detector(self,motor,detector):
        self.name_detector = detector
        self.name_motor_x = motor
        #print(self.name_motor_x,self.name_detector)
    def update_plt_data(self,data_xbpm):
        sum_xbpm = self.get_sum_xbpm(data_xbpm)
        sum_x_up,sum_x_down,up_x_down = self.sum_up_xbpm(data_xbpm)
        sum_x_left,sum_x_right,left_x_right = self.sum_left_xbpm(data_xbpm)
        self.sum_xbpm.append(sum_xbpm)
        self.sum_x_up.append(sum_x_up)
        self.sum_x_down.append(sum_x_down)
        self.up_x_down.append(up_x_down)
        self.sum_x_left.append(sum_x_left)
        self.sum_x_right.append(sum_x_right)
        self.left_x_right.append(left_x_right)
        self.xbpm_A.append(data_xbpm[0])
        self.xbpm_B.append(data_xbpm[1])
        self.xbpm_C.append(data_xbpm[2])
        self.xbpm_D.append(data_xbpm[3])

        self.tot_sum_xbpm.append(sum_xbpm)
        self.tot_sum_x_up.append(sum_x_up)
        self.tot_sum_x_down.append(sum_x_down)
        self.tot_up_x_down.append(up_x_down)
        self.tot_sum_x_left.append(sum_x_left)
        self.tot_sum_x_right.append(sum_x_right)
        self.tot_left_x_right.append(left_x_right)
        self.tot_xbpm_A.append(data_xbpm[0])
        self.tot_xbpm_B.append(data_xbpm[1])
        self.tot_xbpm_C.append(data_xbpm[2])
        self.tot_xbpm_D.append(data_xbpm[3])

        
        if self.x_M:
           self.x_axis = list(range(len(self.sum_xbpm)))
           self.tot_x_axis = list(range(len(self.tot_sum_xbpm)))
        self.update_2d_image()
        tot_data = [self.tot_sum_xbpm,self.tot_up_x_down,self.tot_left_x_right]
        if self.y_axis_get:
        #for i in range(len(tot_data)):
            a,b = self.get_max_min(self.tot_x_axis,tot_data[0])
            c,d = self.get_max_min(self.tot_y_axis,tot_data[0])
            labels = 'max= '+'('+str(a[0])+','+str(c[0])+','+str(a[1])+')'+', min ='+'('+str(b[0])+','+str(d[0])+','+str(b[1])+')'
            #labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[0].max_min_label.setText(labels)
            a,b = self.get_max_min(self.tot_x_axis,tot_data[1])
            c,d = self.get_max_min(self.tot_y_axis,tot_data[1])
            labels = 'max= '+'('+str(a[0])+','+str(c[0])+','+str(a[1])+')'+', min ='+'('+str(b[0])+','+str(d[0])+','+str(b[1])+')'
            #labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[4].max_min_label.setText(labels)
            a,b = self.get_max_min(self.tot_x_axis,tot_data[2])
            c,d = self.get_max_min(self.tot_y_axis,tot_data[2])
            labels = 'max= '+'('+str(a[0])+','+str(c[0])+','+str(a[1])+')'+', min ='+'('+str(b[0])+','+str(d[0])+','+str(b[1])+')'
            #labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[5].max_min_label.setText(labels)
        else:
            a,b = self.get_max_min(self.tot_x_axis,tot_data[0])
            labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[0].max_min_label.setText(labels)
            a,b = self.get_max_min(self.tot_x_axis,tot_data[1])
            labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[4].max_min_label.setText(labels)
            a,b = self.get_max_min(self.tot_x_axis,tot_data[2])
            labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[5].max_min_label.setText(labels)
    def update_step_y(self,step_y):
        self.step_y = float(step_y)
    def update_plt_x(self,x):
        self.x_M = False
        self.x_axis.append(x)
        self.tot_x_axis.append(x)
    def update_2d_image(self):
        if (len(self.y_axis)>=2):
           if ((self.y_axis[-1]-self.y_axis[-2])>= 0.5*self.step_y):
                self.sum_xbpm = [self.sum_xbpm[-1]]
                self.sum_x_up = [self.sum_x_up[-1]]
                self.sum_x_down = [self.sum_x_down[-1]]
                self.up_x_down = [self.up_x_down[-1]]
                self.sum_x_left = [self.sum_x_left[-1]]
                self.sum_x_right = [self.sum_x_right[-1]]
                self.left_x_right = [self.left_x_right[-1]]
                self.x_axis = [self.x_axis[-1]]
                #self.y_axis = []
                self.xbpm_A = [self.xbpm_A[-1]]
                self.xbpm_B = [self.xbpm_B[-1]]
                self.xbpm_C = [self.xbpm_C[-1]]
                self.xbpm_D = [self.xbpm_D[-1]]
                self.update_multi_plot(self.xbpm_A,self.xbpm_B,self.xbpm_C,self.xbpm_D,self.sum_xbpm,self.sum_x_up,self.sum_x_down,self.up_x_down,self.sum_x_left,self.sum_x_right,self.left_x_right,self.x_axis)
           else:
                self.update_multi_plot(self.xbpm_A,self.xbpm_B,self.xbpm_C,self.xbpm_D,self.sum_xbpm,self.sum_x_up,self.sum_x_down,self.up_x_down,self.sum_x_left,self.sum_x_right,self.left_x_right,self.x_axis)
              
        else:
           self.plot_items[1].plot.clear()
           self.plot_items[2].plot.clear()
           self.plot_items[3].plot.clear()
           self.update_plot(self.xbpm_A,self.xbpm_B,self.xbpm_C,self.xbpm_D,self.sum_xbpm,self.sum_x_up,self.sum_x_down,self.up_x_down,self.sum_x_left,self.sum_x_right,self.left_x_right,self.x_axis)
    def update_plt_y(self,y):
        self.y_axis_get = True
        #print(y)
        self.y_axis.append(y)
        self.tot_y_axis.append(y)
    def update_multi_plot(self,xbpm_A,xbpm_B,xbpm_C,xbpm_D, sum_xbpm, sum_x_up, sum_x_down, up_x_down, sum_x_left, sum_x_right, left_x_right, x): 
        self.plot_items[0].plot.plot(x,sum_xbpm,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[1].plot.plot(x,xbpm_A,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]))
        self.plot_items[1].plot.plot(x,xbpm_B,pen=pg.mkPen(color=self.color_list[1],width=2),brush=pg.mkBrush(color=self.color_list[1]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[1]),symbolBrush=pg.mkBrush(color=self.color_list[1]))
        self.plot_items[1].plot.plot(x,xbpm_C,pen=pg.mkPen(color=self.color_list[2],width=2),brush=pg.mkBrush(color=self.color_list[2]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[2]),symbolBrush=pg.mkBrush(color=self.color_list[2]))
        self.plot_items[1].plot.plot(x,xbpm_D,pen=pg.mkPen(color=self.color_list[3],width=2),brush=pg.mkBrush(color=self.color_list[3]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[3]),symbolBrush=pg.mkBrush(color=self.color_list[3]))
        
        self.plot_items[2].plot.plot(x,sum_x_up,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]))
        self.plot_items[2].plot.plot(x,sum_x_down,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[4].plot.plot(x,up_x_down,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[3].plot.plot(x,sum_x_left,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]))
        self.plot_items[3].plot.plot(x,sum_x_right,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[5].plot.plot(x,left_x_right,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.save_tif()
        
    def update_plot(self,xbpm_A,xbpm_B,xbpm_C,xbpm_D, sum_xbpm, sum_x_up, sum_x_down, up_x_down, sum_x_left, sum_x_right, left_x_right, x): 
        self.plot_items[0].plot.plot(x,sum_xbpm,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[1].plot.plot(x,xbpm_A,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]),name='I_a')
        self.plot_items[1].plot.plot(x,xbpm_B,pen=pg.mkPen(color=self.color_list[1],width=2),brush=pg.mkBrush(color=self.color_list[1]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[1]),symbolBrush=pg.mkBrush(color=self.color_list[1]),name='I_b')
        self.plot_items[1].plot.plot(x,xbpm_C,pen=pg.mkPen(color=self.color_list[2],width=2),brush=pg.mkBrush(color=self.color_list[2]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[2]),symbolBrush=pg.mkBrush(color=self.color_list[2]),name='I_c')
        self.plot_items[1].plot.plot(x,xbpm_D,pen=pg.mkPen(color=self.color_list[3],width=2),brush=pg.mkBrush(color=self.color_list[3]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[3]),symbolBrush=pg.mkBrush(color=self.color_list[3]),name='I_d')
        
        self.plot_items[2].plot.plot(x,sum_x_up,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]),name='Ia+Ib')
        self.plot_items[2].plot.plot(x,sum_x_down,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)),name='Ic+Id')
        self.plot_items[4].plot.plot(x,up_x_down,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[3].plot.plot(x,sum_x_left,pen=pg.mkPen(color=self.color_list[0],width=2),brush=pg.mkBrush(color=self.color_list[0]),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=self.color_list[0]),symbolBrush=pg.mkBrush(color=self.color_list[0]),name='Ia+Ic')
        self.plot_items[3].plot.plot(x,sum_x_right,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)),name='Ib+Id')
        self.plot_items[5].plot.plot(x,left_x_right,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.save_tif()
        #self.plot_items[2].plot.plot(x,cent_y_pos,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        #self.plot_items[3].plot.plot(x,cent_pos,pen=pg.mkPen(color=(0,0,0),width=2),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=7,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        #self.plot_items[1].plot.legend.addItem(self.plot_items[1].plot.curves[0],'I_a')
    def find_nearest(self,array_x,array_y,value):
        array_x = np.asarray(array_x)
        array_y = np.asarray(array_y)
        idx = (np.abs(array_x-value).argmin())
        return array_x[idx],array_y[idx]
    def init_k_b(self,k_up,b_up,k_left,b_left):
        self.k_up = k_up
        self.b_up = b_up
        self.k_left = k_left
        self.b_left = b_left
    def xbpm_cali(self):
        lin1 = self.infs[0].value()
        lin2 = self.infs[1].value()
        Mup_low = np.min([lin1,lin2])
        Mup_high = np.max([lin1,lin2])
        m1,y1 =  self.find_nearest(self.x_axis,self.up_x_down, Mup_low)
        m2,y2 =  self.find_nearest(self.x_axis,self.up_x_down, Mup_high)
        self.k_up = (y2-y1)/(m2-m1)
        self.b_up = y2-self.k_up*m2

        lin3 = self.infs[2].value()
        lin4 = self.infs[3].value()
        Mleft_low = np.min([lin3,lin4])
        Mleft_high = np.max([lin3,lin4])
        m3,y3 =  self.find_nearest(self.x_axis,self.up_x_down, Mleft_low)
        m4,y4 =  self.find_nearest(self.x_axis,self.up_x_down, Mleft_high)
        self.k_left = (y4-y3)/(m4-m3)
        self.b_left = y4-self.k_left*m4
        self.trigger_xbpm_k_b.emit(self.k_up,self.b_up,self.k_left,self.b_left)
    def get_sum_xbpm(self,data_xbpm):
        sum_xbpm = np.sum(data_xbpm)
        return(sum_xbpm)
    def sum_left_xbpm(self,data_xbpm):
        m = data_xbpm[0]+data_xbpm[2]
        n = data_xbpm[1]+data_xbpm[3]
        sum_dev = self.k_left*((m-n)/(m+n))+self.b_left
        return(m,n,sum_dev)
    def sum_up_xbpm(self,data_xbpm):
        m = data_xbpm[0]+data_xbpm[1]
        n = data_xbpm[2]+data_xbpm[3]
        sum_dev = self.k_up*((m-n)/(m+n))+self.b_up
        return(m,n,sum_dev)
    def clear_show(self):
        self.x_M = True
        self.y_axis_get = False
        self.sum_xbpm = []
        self.sum_x_up = []
        self.sum_x_down = []
        self.up_x_down = []
        self.sum_x_left = []
        self.sum_x_right = []
        self.left_x_right = []
        self.x_axis = []
        self.y_axis = []
        self.xbpm_A = []
        self.xbpm_B = []
        self.xbpm_C = []
        self.xbpm_D = []
        self.tot_sum_xbpm = []
        self.tot_sum_x_up = []
        self.tot_sum_x_down = []
        self.tot_up_x_down = []
        self.tot_sum_x_left = []
        self.tot_sum_x_right = []
        self.tot_left_x_right = []
        self.tot_x_axis = []
        self.tot_y_axis = []
        self.tot_xbpm_A = []
        self.tot_xbpm_B = []
        self.tot_xbpm_C = []
        self.tot_xbpm_D = []
        for i in range((math.ceil(self.n_index/2))*2):
            self.plot_items[i].plot.clear()

    def get_max_min(self,list_x,list_y):
        max_a = list_y.index(max(list_y))
        min_a = list_y.index(min(list_y))
        #print(max_a)
        
        max_pos = (float("%.8f" % float(list_x[max_a])), float( "%.8f" % list_y[max_a]))
        min_pos = (float("%.8f" %list_x[min_a]), float( "%.8f" % list_y[min_a]))
        #print(max_pos,min_pos)
        return(max_pos,min_pos)            
    def save_tif(self):
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_path = self.save_path
        try:
              with open("/home/mamba/FS_tif/center_xbpm.txt","a") as f:
                  if self.y_axis_get:
                      f.writelines(self.name_motor_x +" "+"%13.8f" % self.x_axis[-1]+" "+self.name_motor_y+" "+"%13.8f" % self.y_axis[-1]+" "+ self.name_detector+" "+ "%13.8f" % self.xbpm_A[-1]+" "+"%13.8f" % self.xbpm_B[-1]+" "+"%13.8f" % self.xbpm_C[-1]+" "+"%13.8f" % self.xbpm_D[-1]+" "+"%13.8f" % self.sum_xbpm[-1]+" "+"%13.8f" % self.sum_x_up[-1]+" "+"%13.8f" % self.sum_x_down[-1]+" "+"%13.8f" % self.up_x_down[-1]+" "+"%13.8f" % self.sum_x_left[-1]+" "+"%13.8f" % self.sum_x_right[-1]+" "+"%13.8f" % self.left_x_right[-1]+" "+time_now)
                  else:
              
                      f.writelines(self.name_motor_x+" "+"%13.8f" % self.x_axis[-1]+" "+self.name_detector+" "+"%13.8f" % self.xbpm_A[-1]+" "+"%13.8f" % self.xbpm_B[-1]+" "+"%13.8f" % self.xbpm_C[-1]+" "+"%13.8f" % self.xbpm_D[-1]+" "+"%13.8f" % self.sum_xbpm[-1]+" "+"%13.8f" % self.sum_x_up[-1]+" "+"%13.8f" % self.sum_x_down[-1]+" "+"%13.8f" % self.up_x_down[-1]+" "+"%13.8f" % self.sum_x_left[-1]+" "+"%13.8f" % self.sum_x_right[-1]+" "+"%13.8f" % self.left_x_right[-1]+" "+time_now) 
                  
                  f.writelines("\n")
        except:
              self.name_motor_x = 'count'
              self.name_detector = 'XBPM'
              with open("/home/mamba/FS_tif/center_xbpm.txt","a") as f:
                  if self.y_axis_get:
                      f.writelines(self.name_motor_x +" "+"%13.8f" % self.x_axis[-1]+" "+self.name_motor_y+" "+"%13.8f" % self.y_axis[-1]+" "+ self.name_detector+" "+ "%13.8f" % self.xbpm_A[-1]+" "+"%13.8f" % self.xbpm_B[-1]+" "+"%13.8f" % self.xbpm_C[-1]+" "+"%13.8f" % self.xbpm_D[-1]+" "+"%13.8f" % self.sum_xbpm[-1]+" "+"%13.8f" % self.sum_x_up[-1]+" "+"%13.8f" % self.sum_x_down[-1]+" "+"%13.8f" % self.up_x_down[-1]+" "+"%13.8f" % self.sum_x_left[-1]+" "+"%13.8f" % self.sum_x_right[-1]+" "+"%13.8f" % self.left_x_right[-1]+" "+time_now)
                  else:
              
                      f.writelines(self.name_motor_x+" "+"%13.8f" % self.x_axis[-1]+" "+self.name_detector+" "+"%13.8f" % self.xbpm_A[-1]+" "+"%13.8f" % self.xbpm_B[-1]+" "+"%13.8f" % self.xbpm_C[-1]+" "+"%13.8f" % self.xbpm_D[-1]+" "+"%13.8f" % self.sum_xbpm[-1]+" "+"%13.8f" % self.sum_x_up[-1]+" "+"%13.8f" % self.sum_x_down[-1]+" "+"%13.8f" % self.up_x_down[-1]+" "+"%13.8f" % self.sum_x_left[-1]+" "+"%13.8f" % self.sum_x_right[-1]+" "+"%13.8f" % self.left_x_right[-1]+" "+time_now) 
                  
                  f.writelines("\n")
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    w = xbpm_widget(3)
    w.show()
    sys.exit(app.exec_())
