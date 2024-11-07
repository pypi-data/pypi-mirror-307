#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame,QLineEdit,QComboBox,QGridLayout,QGroupBox,QMainWindow,QRadioButton, QToolBar
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QSize, QRectF, QPointF
from PyQt5.QtGui import  QFont,QColor, QPixmapCache, QIcon, QPen
import random
import sys
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget, mkPen, mkBrush
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from .QWidget_widget import FxBpmImage,MyImageItem,MyImageView,MyROI,InteractiveViewBoxC
from  .CurvePlot_widget import CurvePlot
import numpy as np
from .math_func import math_func
import datetime
from PIL import Image
class image_show(QWidget):
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
        self.math_func = math_func()
        self.y_axis_name = ['cent_x','cent_y','cent','sum']
        self.plot_items = []
        #self.vbox_plt = QVBoxLayout()
        self.vbox_plt = QGridLayout()
        self.plotimg_item = pg.PlotItem()
        self.ADDROI = True

        self.y_axis_get = False
        
        self.win_image2D = pg.GraphicsLayoutWidget()
        self.img = pg.ImageItem()
        self.p1 = self.win_image2D.addPlot()#(title='Plot-2D(面探测器图像)')
        self.p1.addItem(self.img)
        self.p1.setLabel('bottom','X')
        self.p1.setLabel('left','Y')
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.hist.autoHistogramRange = True
        self.win_image2D.addItem(self.hist)
        
        self.win_image2D.setMouseTracking(True)
        #self.set_level_edit()
        def mousePressEvent(event):
            if self.ADDROI:
                if event.button() == Qt.LeftButton:
                    self.ROI_add()
                    self.ADDROI = False
        self.win_image2D.scene().sigMouseClicked.connect(mousePressEvent)
        

        self.n_index = n
        for j in range(2):
            for i in range(self.n_index-1):
                self.plot_item = CurvePlot()
                if (j==1):
                   if (i ==2):
                      self.vbox_plt.addWidget(self.plot_item,i,j,1,1)
                      self.plot_item.set_axis_name("M",self.y_axis_name[-1])
                      self.plot_items.append(self.plot_item)
                   else:
                      self.vbox_plt.addWidget(self.win_image2D,i,j,2,1)
                else:
                   self.plot_items.append(self.plot_item)
                   self.plot_item.set_axis_name("M",self.y_axis_name[i])
                   self.vbox_plt.addWidget(self.plot_item,i,j,1,1)
        
        self.save_path = "/home/mamba/FS_tif"
        self.image_show = None
        self.show_range = None
        self.auto_level = True
        self.roi = None
        self.hbox = QHBoxLayout()
        #vbox.setContentsMargins(0, 0, 0, 0)
        #vbox.addWidget(self.navbar)
        self.hbox.addLayout(self.vbox_plt,1)
        #self.hbox.addWidget(self.image_view,1)
        #self.hbox.addLayout(self.p1)
        #self.hbox.addWidget(self.win_image2D,1)
        #self.setLayout(vbox)
        groupbox1 = QGroupBox("")
        groupbox1.setLayout(self.hbox)
        twogroup = QHBoxLayout()
        twogroup.addWidget(groupbox1)
        self.setLayout(twogroup)
        #self.show()
    def clear_show(self):
        self.x_M = True
        self.sum_roi = []
        self.cent_x_pos = []
        self.cent_y_pos = []
        self.cent_pos = []
        self.x_axis = []
        self.y_axis = []
         
        self.tot_sum_roi = []
        self.tot_cent_x_pos = []
        self.tot_cent_y_pos = []
        self.tot_cent_pos = []
        self.tot_x_axis = []
        self.tot_y_axis = []
        
        for i in range(self.n_index):
            self.plot_items[i].plot.clear()
    def getXywh(self):
        self.show_range = [int(self.roi.pos()[0]),int(self.roi.pos()[0]+self.roi.size()[0]),int(self.roi.pos()[1]),int(self.roi.pos()[1]+self.roi.size()[1])]
        #self.show_range = (tuple((x) for x in tuple(self.roi.pos()) + tuple(self.roi.size())))
        print(self.show_range)
        self.roi_image()
    def roi_image(self):
        self.roi_img = self.image[self.show_range[0]:self.show_range[1],self.show_range[2]:self.show_range[3]]
        #print(len(self.roi_img))
        return(np.sum(self.roi_img))
    def update_plot(self,sum_roi,cent_x_pos,cent_y_pos,cent_pos,x):
        #print(sum_roi,cent_x_pos,cent_y_pos,cent_pos,x)
        self.plot_items[3].plot.plot(x,sum_roi,pen=pg.mkPen(color=(0,0,0),width=3),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=10,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[0].plot.plot(x,cent_x_pos,pen=pg.mkPen(color=(0,0,0),width=3),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=10,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[1].plot.plot(x,cent_y_pos,pen=pg.mkPen(color=(0,0,0),width=3),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=10,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
        self.plot_items[2].plot.plot(x,cent_pos,pen=pg.mkPen(color=(0,0,0),width=3),brush=pg.mkBrush(color=(0,0,0)),symbol='o',symbolSize=10,symbolPen=pg.mkPen(color=(0,0,0)),symbolBrush=pg.mkBrush(color=(0,0,0)))
    def update_image_show(self, image):
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.image = np.array(image)
        self.image_show = True
        image_max = np.max(self.image)
        image_mean = np.mean(self.image)
        self.img.setImage(self.image,autoRange=True,autoHistogramRange=True)
    def update_image_data(self, image):
        self.image = np.array(image)
        self.image_show = True
        #image_max = np.max(self.image)
        #image_mean = np.mean(self.image)
        #log_image = np.log10(self.image)
        #log_image = self.image
        #self.img.setImage(log_image,autoRange=True,autoHistogramRange=True)
        if self.roi:
            self.getXywh()
            sum_roi = self.roi_image()
            cent_x_pos,cent_y_pos,cent_pos = self.math_func.cent_w(self.roi_img)
        else:
            sum_roi = np.sum(self.image)
            cent_x_pos,cent_y_pos,cent_pos = self.math_func.cent_w(self.image)
        #print(cent_x_pos,cent_y_pos,cent_pos)
        self.sum_roi.append(sum_roi)
        self.cent_x_pos.append(cent_x_pos)
        self.cent_y_pos.append(cent_y_pos)
        self.cent_pos.append(cent_pos)
        self.tot_sum_roi.append(sum_roi)
        self.tot_cent_x_pos.append(cent_x_pos)
        self.tot_cent_y_pos.append(cent_y_pos)
        self.tot_cent_pos.append(cent_pos)
        
        if self.x_M:
           self.x_axis = list(range(len(self.sum_roi)))
           self.tot_x_axis = list(range(len(self.tot_sum_roi)))


        tot_data = [self.tot_cent_x_pos,self.tot_cent_y_pos,self.tot_cent_pos,self.tot_sum_roi]
        for i in range(len(tot_data)):
            a,b = self.get_max_min(self.tot_x_axis,tot_data[i])
            if self.y_axis_get :
                c,d = self.get_max_min(self.tot_y_axis,tot_data[i])
                labels = 'max= '+'('+str(a[0])+','+str(c[0])+','+str(a[1])+')'+', min ='+'('+str(b[0])+','+str(d[0])+','+str(b[1])+')'
            else:
                labels = 'max= '+str(a)+', min ='+str(b)
            self.plot_items[i].max_min_label.setText(labels)
        self.update_2d_image()
        self.update_plot(self.sum_roi,self.cent_x_pos,self.cent_y_pos,self.cent_pos,self.x_axis)
        self.save_tif()
    def update_motor_detector(self,motor_x,detector):
        self.name_detector = detector
        self.name_motor_x = motor_x
        #self.name_motor_y = motor_y
    def update_2d_motor_detector(self,motor_y,motor_x,detector):
        self.name_detector = detector
        self.name_motor_x = motor_x
        self.name_motor_y = motor_y
        print(self.name_detector,self.name_motor_x,self.name_motor_y)
    def update_step_y(self,step_y):
        self.step_y = float(step_y)
    def update_plt_y(self,y):
        self.y_axis_get = True
        #print(y)
        self.y_axis.append(y)
        self.tot_y_axis.append(y)
              #self.y_axis = []
    def update_2d_image(self):
        if (len(self.y_axis)>=2):
           if ((self.y_axis[-1]-self.y_axis[-2])>= 0.5*self.step_y):
              self.sum_roi = [self.sum_roi[-1]]
              self.cent_x_pos = [self.cent_x_pos[-1]]
              self.cent_y_pos = [self.cent_y_pos[-1]]
              self.cent_pos = [self.cent_pos[-1]]
              self.x_axis = [self.x_axis[-1]]
       
    def update_image_x(self,x):
        self.x_M = False
        self.x_axis.append(x)
        self.tot_x_axis.append(x)
        #return(self.x_axis)

    def get_max_min(self,list_x,list_y):
        max_a = list_y.index(max(list_y))
        min_a = list_y.index(min(list_y))
        #print(max_a)
        
        max_pos = (float("%.4f" % float(list_x[max_a])), float( "%.4f" % list_y[max_a]))
        min_pos = (float("%.4f" %list_x[min_a]), float( "%.4f" % list_y[min_a]))
        #print(max_pos,min_pos)
        return(max_pos,min_pos)
    def ROI_add(self):
        #print(self.image)
        if self.image_show:
           self.pixel_pos_x = int(self.image.shape[0] *0.4)
           self.pixel_pos_y = int(self.image.shape[1] *0.4)
           self.pixel_size_x = int(self.image.shape[0] *0.1)
           self.pixel_size_y = int(self.image.shape[1] *0.1)
        else:
           self.pixel_pos_x = 0
           self.pixel_pos_y = 0
           self.pixel_size_x = 10
           self.pixel_size_y = 10
        self.roi = MyROI([self.pixel_pos_x, self.pixel_pos_y],[self.pixel_size_x, self.pixel_size_y],maxBounds=QtCore.QRectF(-1000000, -10000000, 1000000000000, 1000000000),pen = pg.mkPen((3,3), width=5.), removable = True)
        self.roi.sigRegionChangeFinished.connect(lambda: self.getXywh())
        self.p1.addItem(self.roi)       
        self.p1.update()
    def update_save_path(self, save_path):
        self.save_path = save_path
    def save_tif(self):
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_path = self.save_path
        #print(save_path)
        #save_file_x = str(self.x_axis[-1])
        #save_file_y = str(self.y_axis[-1]
        #if self.name_motor_x == 0:
        #    self.name_motor_x = 'count'
        try:   
              if self.y_axis:
                  save_file = save_path+ "/" +self.name_motor_x+ str(self.x_axis[-1])+" "+self.name_motor_y + str(self.y_axis[-1])+self.name_detector+" "+time_now
              else:
                  save_file = save_path + "/"+self.name_motor_x+str(self.x_axis[-1])+self.name_detector +" "+time_now
              #print(save_file)
              with open("/home/mamba/FS_tif/center_Fs.txt","a") as f:
                  if self.y_axis:
                      f.writelines(self.name_motor_x +"%13.8f" % self.x_axis[-1]+" "+self.name_motor_y +"%13.8f" % self.y_axis[-1]+" "+self.name_detector +" "+"%13.8f" % self.sum_roi[-1]+" "+"%13.8f" % self.cent_x_pos[-1]+" "+"%13.8f" % self.cent_y_pos[-1]+" "+"%13.8f" % self.cent_pos[-1]+" "+time_now)
                  else:
                      f.writelines(self.name_motor_x +"%13.8f" % self.x_axis[-1]+" "+self.name_detector +"%13.8f" % self.sum_roi[-1]+" "+"%13.8f" % self.cent_x_pos[-1]+" "+"%13.8f" % self.cent_y_pos[-1]+" "+"%13.8f" % self.cent_pos[-1]+" "+time_now)
                  #f.writelines("%11.8f" % float(save_file_x)+"%15.8f" %  float(save_file_y)+"     "+time_now)
                  f.writelines("\n")
              try:
                  Image.fromarray(self.image).save(save_file+".tif")
                  Image.fromarray(self.image).save(save_file+".png")
              #try:
              #    Image.fromarray(self.image).save(save_file+".tif")
              except:
                  print("error")
        except:
              self.name_motor_x = 'count '
              self.name_detector = 'FS  '
              if self.y_axis:
                  save_file = save_path+ "/" +self.name_motor_x+ str(self.x_axis[-1])+" "+self.name_motor_y + str(self.y_axis[-1])+self.name_detector+" "+time_now
              else:
                  save_file = save_path + "/"+self.name_motor_x+str(self.x_axis[-1])+self.name_detector +" "+time_now
              #print(save_file)
              with open("/home/mamba/FS_tif/center_Fs.txt","a") as f:
                  if self.y_axis:
                      f.writelines(self.name_motor_x +"%13.8f" % self.x_axis[-1]+" "+self.name_motor_y +"%13.8f" % self.y_axis[-1]+" "+self.name_detector +" "+"%13.8f" % self.sum_roi[-1]+" "+"%13.8f" % self.cent_x_pos[-1]+" "+"%13.8f" % self.cent_y_pos[-1]+" "+"%13.8f" % self.cent_pos[-1]+" "+time_now)
                  else:
                      f.writelines(self.name_motor_x +"%13.8f" % self.x_axis[-1]+" "+self.name_detector +"%13.8f" % self.sum_roi[-1]+" "+"%13.8f" % self.cent_x_pos[-1]+" "+"%13.8f" % self.cent_y_pos[-1]+" "+"%13.8f" % self.cent_pos[-1]+" "+time_now)
                  #f.writelines("%11.8f" % float(save_file_x)+"%15.8f" %  float(save_file_y)+"     "+time_now)
                  f.writelines("\n")
              try:
                  Image.fromarray(self.image).save(save_file+".tif")
                  Image.fromarray(self.image).save(save_file+".png")
              #try:
              #    Image.fromarray(self.image).save(save_file+".tif")
              except:
                  print("error")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    w = image_show(4)
    img = np.array([[random.randrange(10,100,2)
                              for j in range(0,1024)]
                             for i in range(0,1024)])
    w.updata_image2D(img)
    w.show()
    sys.exit(app.exec_())
