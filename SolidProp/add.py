import os
import os.path as op
import sys
import json
import string
import numpy as np
import PropertySI as ps
#import tk

thispath = op.abspath(op.dirname(__file__))
datapath = op.join(thispath, 'PropData')
suffix = '.json'
pun = string.punctuation
current = ps.prop_names()


#Takes the dict and makes it key value pairs
def make_jobj(newData):
    dataTuple = tuple(open(newData))
    dats = [d.strip(pun) for d in dataTuple[0].split() if '[' not in d]
    vals = np.genfromtxt(newData, skip_header=1)
    Td = vals[:,0]
    dc = dict()
    for i, nm in enumerate(dats[1:]):
        dc[nm] = np.vstack((Td, vals[:,i+1])).tolist()
        
    return dc


class GUI:
    def __init__(self, app): 
        self.app = app
        app.title("THANK YOU FOR CONTRIBUTING TO SOLIDPROP!")
        
        #WIP
        
#        jLoad = json.load(db)
#
#        #Button, entry boxes, radio button, file chooser.
#
#        #if loading a file
#        db = op.join(thispath, 'solidProps.json')
#        gwon = np.genfromtxt(chosenFile, delim_whitespace=True)
#        db[mats] = gwon #Also need to split by key.  Maybe just read in normal and convert to numpy
#        jLoad.dumps(db)
        

if __name__ == "__main__":
    
    
#    if len(sys.argv) < 2:
#        
#        master = tk.Tk()
#        GUI(master)
#        master.mainloop()
#        
#    else:
        
        tDatapath = op.join(datapath, 'temp')
        for file in os.listdir(tDatapath):
            if file.lower().endswith(".txt") and file.lower() not in current:
                
                f = file.split('.')[0].upper()  
                fnow = op.join(tDatapath, file)
                propFile = op.join(datapath, f.upper() + suffix)
                boy = make_jobj(fnow)
                with open(propFile, 'w') as dr:
                    json.dump(boy, dr)



