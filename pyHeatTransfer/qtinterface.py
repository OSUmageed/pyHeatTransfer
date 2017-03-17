#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path as op
import sys
from PyQt5 import QtWidgets, QtGui

sourcepath = op.abspath(op.dirname(__file__))
gitpath = op.dirname(sourcepath) #Top level of git repo
os.chdir(sourcepath)
sys.path.append(gitpath)

import numpy as np
import SolidProp.PropertySI as sp
import conduction as cd
import examples as ex

solidpath = op.join(gitpath, 'SolidProp')
datapath = op.join(solidpath, 'PropData')
MATERIALS = sp.prop_names()

class Window(QtWidgets.QWidget):
    mats = MATERIALS
    toK = 273.15   

    def __init__ (self):
        super(Window, self).__init__()
        #Now the Window is the self.
        self.setGeometry(50, 50, 500, 800)
        self.butt = QtWidgets.QPushButton(self)
        self.butt.setText( 'Start Application')
        self.setWindowTitle("New pyHeat GUI")
        self.Lbl = QtWidgets.QLabel(self)
        self.Lbl.setText(self.mats[0])
        self.Lbl.move(100, 90)
        self.show()
        
#OK
app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
        