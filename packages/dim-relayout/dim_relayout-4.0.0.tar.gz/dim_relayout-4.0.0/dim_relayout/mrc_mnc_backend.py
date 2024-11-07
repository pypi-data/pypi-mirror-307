
import numpy as np
import math
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
import random
from PyQt5.QtCore import pyqtSignal
import datetime



class mrc_mnc(QWidget):
    #trigger_oneD_scan_status = pyqtSignal(str)
    #trigger_twoD_scan_status = pyqtSignal(str)
    def __init__(self,mrc,mnc,parent=None):
        super().__init__(parent)
        self.mrc = mrc
        self.mnc = mnc
        self.detector_image = ['D.WhiteFS','D.IntegratedFS', 'D.MonochromaticFS', 'D.HRFS1', 'D.HRFS2']
        self.detector_point = ['电离室']
        self.detector_xbpm = ['D.WhiteXBPM','D.QXBPM']
        #m = {'extra':{'type': 'detector_scan_start', 'mode': 'prepare', 'detector': D_name}}
        #command = "P.grid_scan(["+D_backend_str.strip("''")+",D.ct08],M.BraggTheta,"+ str(theta_start) + ","+str(theta_end) +","+str(n_step)+",md =" + str(m) +")\n"
############################################################################
    def D_set_time(self,D_name,D_time):
        D_name = str(D_name)
        
        if D_name in self.detector_image:
            command_time =  "%go "+ D_name+".cam.acquire_time.set(" + str(D_time) + ").wait()\n"
            self.mrc.do_cmd(command_time)
        else:
            pass
            #command_time =  D_name+".acquire_time.set(" + str(D_time) + ").wait()\n"
        #print(command_time)
    def D_image_cam(self,D_name):
        cmd_monitor =  "%go "+ D_name +".cam.acquire.set(%d).wait()\n" % int(0)
            #self.mrc.req_rep_base("cmd", go = "", cmd = cmd_monitor)
        self.mrc.do_cmd(cmd_monitor)   
###############################################################################
    def D_start(self,D_name,D_time,D_loop,scantype):
        if D_name in self.detector_image:
            cmd_monitor =  "%go "+ D_name +".cam.acquire.set(%d).wait()\n" % int(0)
            #self.mrc.req_rep_base("cmd", go = "", cmd = cmd_monitor)
            self.mrc.do_cmd(cmd_monitor)
        else:
            pass
        self.D_set_time(D_name,D_time)
        #D_name = str(D_name)
        #command_time =  D_name+".acquire_time.set(" + str(D_time) + ").wait()\n"
        #self.mrc.do_cmd(command_time)
        #D_loop = int(D_loop)
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        save_path = '/home/mamba/mdw_result/experiment'+time_now
        save_file_name = 'master.nxs'
        m = {'extra':{'hyktype': 'detector_count', 'mode':str(scantype), 'detector': D_name },'filepath_store_dir':save_path,'filepath_store_filename':save_file_name}
        #for i in range (D_loop):
        command_count = "P.count([" + D_name +"], "+ D_loop  + ",md =" + str(m) +")\n"
        self.mrc.req_rep_base("cmd", go = "", cmd = command_count)
    def D_end(self):
        try:
           self.mrc.req_rep("scan/abort")
        except:
           pass
    def D_pause(self):
        self.mrc.req_rep("scan/pause")
    def D_resume(self):
        self.mrc.req_rep("scan/resume")
############################################################################
    def oneD_scan_start(self,M_name,M_start,M_end,M_n_step,D_name,D_exp):
        if D_name in self.detector_image:
            cmd_monitor =  "%go "+ D_name +".cam.acquire.set(%d).wait()\n" % int(0)
            #self.mrc.req_rep_base("cmd", go = "", cmd = cmd_monitor)
            self.mrc.do_cmd(cmd_monitor)
        else:
            pass
        #cmd_monitor =  "%go "+ D_name +".cam.acquire.set(%d).wait()\n" % int(0)
        #self.mrc.req_rep_base("cmd", go = "", cmd = cmd_monitor)
        #self.mrc.do_cmd(cmd_monitor)
        Mone = M_name.replace('.','_',1)
        self.D_set_time(D_name,D_exp)
        #m = {"hyktype": "detector_scan_start" , "frame_count":5000,"scan_type":"stepscan","extra":"scan"}
        #m = {'extra':{'hyktype': 'detector_scan_start', 'mode': 'oneD', 'detector': D_name, 'Motor':Mone}}
        #print(m)
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        save_path = '/home/mamba/mdw_result/experiment'+time_now
        save_file_name = 'master.nxs'
        m = {'extra':{'hyktype': 'detector_count', 'mode':'oneD', 'detector': D_name },'filepath_store_dir':save_path,'filepath_store_filename':save_file_name}
        #mdw_req_cmd_gui(cmds = m)
        #print("5$$$")#self.mrc.req_rep_base("cmd", go = "", cmd = command)    
        command = "P.grid_scan(["+str(D_name) +"],"+str(M_name)+"," + str(M_start) + ","+str(M_end) +","+str(M_n_step)+",md ="+ str(m) +")\n"
        #print(command)
        self.mrc.req_rep_base("cmd", go = "", cmd = command) 
    def twoD_scan_start(self,M_name,M_start,M_end,M_n_step,M2_name,M2_start,M2_end,M2_n_step,D_name,D_exp):
        Mone = M_name.replace('.','_',1)
        Mtwo = M2_name.replace('.','_',1)
        #print(Mone,Mtwo)
        self.D_set_time(D_name,D_exp)
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        save_path = '/home/mamba/mdw_result/experiment'+time_now
        save_file_name = 'master.nxs'
        #m = {'extra':{'hyktype': 'detector_count', 'mode':str(scantype), 'detector': D_name },'filepath_store_dir':save_path,'filepath_store_filename':save_file_name}
        m = {'extra':{'hyktype': 'detector_scan_start', 'mode': 'twoD', 'detector': D_name, 'Motor':(Mone,Mtwo)},'filepath_store_dir':save_path,'filepath_store_filename':save_file_name}
        command = "P.grid_scan(["+str(D_name) +"],"+str(M_name)+"," + str(M_start) + ","+str(M_end) +","+str(M_n_step)+','+str(M2_name)+"," + str(M2_start) + ","+str(M2_end) +","+str(M2_n_step)+",snake_axes = False, md =" + str(m)+")\n"
        #print(command)
        self.mrc.req_rep_base("cmd", go = "", cmd = command)

###################################################################################

    def oneD_scan_end(self):
        self.mrc.req_rep("scan/abort")
        #self.trigger_oneD_scan_status.emit('oneD_scan_end')
        #print("oneD_scan_end")
    def oneD_scan_pause(self):
        self.mrc.req_rep("scan/pause")
        #self.trigger_oneD_scan_status.emit('oneD_scan_pause')
    def oneD_scan_resume(self):
        self.mrc.req_rep("scan/resume")
        #self.trigger_oneD_scan_status.emit('oneD_scan_resume')
    def twoD_scan_end(self):
        self.mrc.req_rep("scan/abort")
        #self.trigger_twoD_scan_status.emit('twoD_scan_end')
    def twoD_scan_pause(self):
        self.mrc.req_rep("scan/pause")
        #self.trigger_twoD_scan_status.emit('twoD_scan_pause')
    def twoD_scan_resume(self):
        self.mrc.req_rep("scan/resume")
        #self.trigger_twoD_scan_status.emit('twoD_scan_resume')
##########################################################################
    def set_M(self,M_name,M_pos):
        cmd = "%go "+ M_name +".set(%f).wait()\n" % float(M_pos)
        #print(cmd)
        self.mrc.do_cmd("%go "+ M_name +".set(%f).wait()\n" % float(M_pos))
    def stop_M(self, M_name):
        cmd = "%go "+ M_name +".stop() \n"
        self.mrc.do_cmd("%go "+ M_name +".stop() \n")
    def limit_M_pos(self,M_name):
        pos_limit_dic = self.mrc.req_rep("dev/read_configuration", path = M_name)["ret"]
        #print(pos_limit_dic)
        try:
            pos_high = pos_limit_dic[M_name+'.high_limit_travel']['value']
            pos_low = pos_limit_dic[M_name+'.low_limit_travel']['value']
        except:
            pos_high = 10000.0
            pos_low = -10000.0
        return(pos_high,pos_low)
    def get_M_pos(self,M_name):
        cmd = "dev/read"+", path = " + M_name
        try:
            pos_now_dic = self.mrc.req_rep("dev/read", path = M_name)["ret"]
            pos_limit_dic = self.mrc.req_rep("dev/read_configuration", path = M_name)["ret"]
        except:
            pass
            #print("please check M name")
        #print(pos_limit_dic)
        try:
            pos_unit = pos_limit_dic[M_name+'.motor_egu']['value']
        except:
            pos_unit = 'degree'
        try:
            pos_now = pos_now_dic[M_name+'.readback']['value']
        except:
            pos_now = 0.0
        #print(pos_now,pos_unit)
        return(pos_now,pos_unit)
    def get_M_list(self):
        motor_name = self.mrc.req_rep("dev/keys", path = "M")["ret"]
        #detector_name = self.mrc.req_rep("dev/keys", path = "D")["ret"]
        return(motor_name)
    def get_D_list(self):
        detector_name = self.mrc.req_rep("dev/keys", path = "D")["ret"]
        #detector_name = self.mrc.req_rep("dev/keys", path = "D")["ret"]
        return(detector_name)
