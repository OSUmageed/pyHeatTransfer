import os
import os.path as op
import sys

import json
import numpy as np

thispath = op.abspath(op.dirname(__file__))
datapath = op.join(thispath, 'PropData')
suffix = '.json'

def get_props(mat):
    db = op.join(datapath, mat+suffix)
    jm = json.load(db)
    return jm

