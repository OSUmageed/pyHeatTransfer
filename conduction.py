import os
import os.path as op
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import SolidProp.PropertySI as sp
import collections
from deco import concurrent, synchronized

thispath = op.abspath(op.dirname(__file__))

#Pattern should be dict sp[material][property] = [[T, val]] 2D numpy
#Would be better to store thermal diffusivity too.
#Would be much better to have a function in a dict for each point in SolidProperties.
#Or at least in a separate funciton.

def make_grid(nx, ny, nz, Ti):
    gr = [[[(x,y,z) for x in range(nx)] for y in range(ny)] for z in range(nz)]
    Tmake = {g : Ti for g in gr} 
    return Tmake
    
@concurrent
def step_forward(Tg_in, Tg_out, Pg, dt_ds):
    st_make = np.array([[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]])
    for gridpt in Tg_in.key():
        Fo = dt_ds*Pg['K']/(Pg['CP']*Pg['D'])
        stencil = [tuple(gb) for gb in np.array(gridpt)+st_make]
        if 0 in gridpt:
            pass
            #boundary condition
        else:
            Tg_out[gridpt] = Fo * sum([Tg_in[s] for s in stencil]) + (1.0 - Fo*6.0)*Tg_in[gridpt]
        
@synchronized
def forward_call(Tg_in, Tg_out, Pg, dt, ds):
    pass

#could use scipy interpolate to do a spline.  This is limited to just linear.
class SolidProperties(object):
    props = ['K', 'CP', 'D']
    def __init__(self, mat, Tgrid):
        self.pRange = sp.get_props(mat)
        self.epsilon = sp.get_props(mat)['E']
        self.pGrid = collections.defaultdict()
        self.update_props(Tgrid)
        
    def update_props(self, Tgrid):
        for pt in self.pGrid:
            for prop in self.props:
                self.pGrid[pt][prop] = np.interp(Tgrid[pt], self.pRange[prop][0, :], 
                                       self.pRange[prop][:, 1])
            
            
        
        
        
        
    
    



