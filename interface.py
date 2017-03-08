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
from kivy.graphics.vertex_instructions import Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Color
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.garden.graph import ContourPlot

from kivy.uix.spinner import Spinner

import numpy as np
import SolidProp.PropertySI as sp
import conduction as cd
import examples as ex

thispath = op.abspath(op.dirname(__file__))
solidpath = op.join(thispath, 'SolidProp')
datapath = op.join(solidpath, 'PropData')

MATERIALS = sp.prop_names()

class TransientHeat(BoxLayout):

    mats = MATERIALS

    def __init__(self,):
        super(TransientHeat, self).__init__()
        self.plot = ContourPlot(color=[1, 0, 0, 1])
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

        print(cd.initialize(self.parameter_dict))
        raise SystemExit


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