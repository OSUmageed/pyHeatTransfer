import os
import os.path as op
import sys

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.garden.graph import ContourPlot
from kivy.uix.spinner import Spinner

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

class TransientHeat(BoxLayout):

    mats = MATERIALS
    toK = 273.15

    def __init__(self,):
        super(TransientHeat, self).__init__()
        self.plot = ContourPlot()
        self.parameter_dict = ex.zigg

    def start(self):
        #Plot should be somewhere else
        self.ids.graphcontour.add_plot(self.plot)

        for i in self.ids.keys():
            if 'graph' not in i:
                try:
                    self.parameter_dict[i] = float(self.ids[i].text)
                except:
                    self.parameter_dict[i] = self.ids[i].text
            
        #Test Part
        cd.initialize_class(self.parameter_dict)

        # self.sim = cd.HeatSimulation(self.parameter_dict)
        # self.yplane = float(self.ids.Ly.text)//2

        # #Until here this part should be on focus (ish) and it should produce a 3D figure in the first plot.  

        # #Now this should be the 'start' function.  It uses the methods of self.sim which is already instantiated, to advance the simulation and it should contain a loop, but we want pause to be able to interrupt it.

        # #self.plot.xrange = self.sim.xrng 
        # #self.plot.yrange = self.sim.yrng
        # while self.sim.tNow < self.sim.tF:
        #     self.sim.step_forward()
        #     self.sim.plot_step(self.yplane)
        #     self.plot.data = self.sim.pPlot
        #     self.ids.middle_label.text = str(self.sim.tNow)
        #     self.plot.draw()
            
        
    def pause(self):
        pass
        
    def shutoff(self, *args):
        raise SystemExit

class HeatApp(App):
    def build(self):
        return TransientHeat()

if __name__ == "__main__":
    HeatApp().run()
    print(MATERIALS)