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
from kivy.lang import Builder
from kivy.properties import ListProperty

import numpy as np
import SolidProp.PropertySI as sp

thispath = op.abspath(op.dirname(__file__))
solidpath = op.join(thispath, 'SolidProp')
datapath = op.join(solidpath, 'PropData')

MATERIALS = sp.prop_names()

class ScatterTextWidget(BoxLayout):
    i=0
    def changeColor(self, *args):
        color = [random.random() for _ in range(3)] + [1]
        label = self.ids['shown']
        label.color = color

    # def printChildren(self, *args):
    #     label = self.ids['shown']
    #     ky = list(self.ids.keys())
    #     v = self.ids[ky[self.i]]
    #     label.text = "key={}, val={}".format(ky[self.i],v)
    #     self.i +=1
        
    def shutoff(self, *args):
        sys.exit()

class HeatApp(App):
    def build(self):
        return ScatterTextWidget()
        # fL = kF.FloatLayout()
        # sC = kS.Scatter()
        # lbl = kL.Label(text=MATERIALS[0], font_size=150)

        # fL.add_widget(sC)
        # sC.add_widget(lbl)
        # return fL

if __name__ == "__main__":
    HeatApp().run()
    print(MATERIALS)