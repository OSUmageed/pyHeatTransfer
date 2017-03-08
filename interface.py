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

thispath = op.abspath(op.dirname(__file__))
solidpath = op.join(thispath, 'SolidProp')
datapath = op.join(solidpath, 'PropData')

MATERIALS = sp.prop_names()


class ScatterTextWidget(BoxLayout):

    #mats = ListProperty(MATERIALS)
    mats = MATERIALS

    def __init__(self,):
        super(ScatterTextWidget, self).__init__()
        #self.spinner = spinner
        #self.mats = MATERIALS
        self.plot = ContourPlot(color=[1, 0, 0, 1])

    def changeColor(self, *args):
        color = [random.random() for _ in range(3)] + [1]
        label = self.ids['shown']
        label.color = color

    def start(self):
        self.ids.graphcontour.add_plot(self.plot)

    def pause(self):
        pass
        
    def shutoff(self, *args):
        raise SystemExit

class HeatApp(App):
    def build(self):
        return ScatterTextWidget()

if __name__ == "__main__":
    HeatApp().run()
    print(MATERIALS)