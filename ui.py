#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from PyQt5.Qt import QProgressBar,QLabel
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import Qt
import time
from bili import down

class meun(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 178)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint,False)
        self.setui()
        self.action()
    def setui(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("AV号",self)
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.qd = QtWidgets.QPushButton("确定",self)
        self.verticalLayout.addWidget(self.qd)
        self.qx = QtWidgets.QPushButton("取消",self)
        self.verticalLayout.addWidget(self.qx)
        self.progressBar = QtWidgets.QProgressBar(self)
        font = QtGui.QFont()
        font.setWeight(70)
        self.progressBar.setFont(font)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.verticalLayout.addWidget(self.progressBar)
        self.progressBar.reset()
    def action(self):
        self.qd.clicked.connect(self.beg)
        self.qx.clicked.connect(lambda : self.close())
    def beg(self):
        if self.lineEdit.text()=="":
            return
        self.mit=down(self.lineEdit.text())
        self.mit.data_.connect(self.bar_set)
        self.mit.start()
    def bar_set(self,value):
        self.progressBar.setValue(value)
        if value==100:
            time.sleep(3)
            self.progressBar.reset()

    
if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    win=meun()
    win.show()
    sys.exit(app.exec_())