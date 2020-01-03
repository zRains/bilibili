#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import time
from msic.bili import down
from msic.demo import set_ui
from msic.get_cover import get_img

class meun(QWidget,set_ui):
    def __init__(self):
        super().__init__()
        self.resize(268, 213)
        self.setWindowTitle("zRain")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint,False)
        #设置默认视频类型
        self.rad_video.setChecked(True)
        #设置默认清晰度
        self.rad_1080.setChecked(True)
        self.action_connect()

    def action_connect(self):
        self.qd.clicked.connect(self.beg)
        self.qx.clicked.connect(lambda : self.close())
        self.rad_acg.clicked.connect(self.lablechange)
        self.rad_video.clicked.connect(self.lablechange)
        self.get_cover.clicked.connect(self.get_covered)
    
    def get_covered(self):
        if self.lineEdit.text()=="":
            return
        self.mit_get_cover=get_img(self.lineEdit.text(),str(self.rad_video.isChecked()),2)
        self.mit_get_cover.pro.connect(self.bar_set)
        self.mit_get_cover.start()

    def lablechange(self):
        if self.rad_video.isChecked():
            self.label.setText("AVID: ")
        if self.rad_acg.isChecked():
            self.label.setText("EPID: ")

    def beg(self):
        video_q=[self.rad_1080,self.rad_720,self.rad_460,self.rad_360]
        count=1
        for i in video_q:
            if i.isChecked():
                break
            count+=1
        if self.lineEdit.text()=="":
            return
        self.mit=down(self.lineEdit.text(),str(self.rad_tr.isChecked()),str(self.rad_del.isChecked()),str(self.rad_video.isChecked()),count)
        self.mit.data_.connect(self.bar_set)
        self.mit.start()

    def bar_set(self,value,stats):
        #设置下载时某些功能不可用
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_3.setEnabled(False)
        self.qd.setEnabled(False)
        all_stats=["下载flv视频文件%p%","下载mp4视频文件%p%","下载m4a音频文件%p%","下载图片中%p%"]
        #设置进度条
        self.progressBar.setFormat(all_stats[stats])
        self.progressBar.setValue(value)
        if value==100:
            self.progressBar.reset()
            self.groupBox.setEnabled(True)
            self.groupBox_2.setEnabled(True)
            self.groupBox_3.setEnabled(True)
            self.qd.setEnabled(True)


    
if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    win=meun()
    win.show()
    sys.exit(app.exec_())
