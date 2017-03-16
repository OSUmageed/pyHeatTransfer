import os 
import os.path as op
import sys

sourcepath = op.abspath(op.dirname(__file__))
sys.path.append(sourcepath)

def main():
    from interface import HeatApp
    HeatApp().run()
    print('Closed pyHeatTransferGUI')
