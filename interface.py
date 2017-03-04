import os
import os.path as op
import sys

from kivy.app import App
import kivy.uix.scatter as kS
import kivy.uix.label as kL
import kivy.uix.floatlayout as kF
import numpy as np
import SolidProp.PropertySI as sp

thispath = op.abspath(op.dirname(__file__))
solidpath = op.join(thispath, 'SolidProp')
datapath = op.join(solidpath, 'PropData')

MATERIALS = sp.prop_names()

class TutorialApp(App):
    def build(self):
        fL = kF.FloatLayout()
        sC = kS.Scatter()
        lbl = kL.Label(text=MATERIALS[0], font_size=150)

        fL.add_widget(sC)
        sC.add_widget(lbl)
        return fL

if __name__ == "__main__":
    TutorialApp().run()
    print MATERIALS