import os
import os.path as op
import sys
import json
import numpy as np
import Tkinter as Tk

thispath = op.abspath(op.dirname(__file__))
datapath = op.join(thispath, 'PropData')


class GUI:
    def __init__(self, app): 
        self.app = app
        app.title("THANK YOU FOR CONTRIBUTING TO SOLIDPROP!")
        jLoad = json.load(db)

        #Button, entry boxes, radio button, file chooser.

        #if loading a file
        db = op.join(thispath, 'solidProps.json')
        gwon = np.genfromtxt(chosenFile, delim_whitespace=True)
        db[mats] = gwon #Also need to split by key.  Maybe just read in normal and convert to numpy
        jLoad.dumps(db)
        



if __name__ == "__main__":
    master = Tk.Tk()
    GUI(master)
    master.mainloop()




