import os
import os.path as op
import sys
import json
import numpy as np

thispath = op.abspath(op.dirname(__file__))
datapath = op.join(thispath, 'PropData')
suffix = '.json'

def prop_names():
    fs = os.listdir(datapath)
    mats = [f.split(".")[0].lower() for f in fs if f.endswith(suffix)]
    return mats

def get_props(mat):
    mat = mat.upper()
    with open(op.join(datapath, mat+suffix), 'r') as db:
        jm = json.load(db)
        
    for key in jm.keys():
        jm[key] = np.array(jm[key])
    return jm

