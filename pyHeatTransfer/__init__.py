import os 
import os.path as op
import sys

sourcepath = op.abspath(op.dirname(__file__))
sys.path.append(sourcepath)

from interface import HeatApp

def main():
    HeatApp().run()
    print('Closed pyHeatTransferGUI')
