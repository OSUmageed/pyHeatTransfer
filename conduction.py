import os
import os.path as op
import sys
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import SolidProp.PropertySI as sp
import collections
from deco import concurrent, synchronized

thispath = op.abspath(op.dirname(__file__))
toK = 273.15

A = [1]
B = [-1]
AB = A+B

typedictionary = collections.defaultdict(dict)

#Would be much better to have a function in a dict for each point in SolidProperties.
#Or at least in a separate funciton.

def make_grid(xi, xf, yi, yf, z, Ti, typestring=""):

    gr = []
    for x in range(xi,xf):
        gr += [(x, y, z) for y in range(yi,yf)] 
        
    Tmake.update(dict.fromkeys(gr, Ti))
    return Tmake, 
    

@concurrent
def step_forward(Tg_in, Tg_out, Pg, qVol, dt_ds, funccGrid):
    st_make = np.array([[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]])
    for gridpt in Tg_in.key():
        Fo = dt_ds*Pg['A']
        stencil = [tuple(gb) for gb in np.array(gridpt) + st_make]
        if 0 in gridpt:
            pass
            #boundary condition
        else:
            Tg_out[gridpt] = Fo * sum([Tg_in[s] for s in stencil]) + (1.0 - Fo*6.0)*Tg_in[gridpt]
        
@synchronized
def forward_call(Tg_in, Tg_out, Pg, qVol, dt_ds, funccGrid):
    pass

#could use scipy interpolate to do a spline.  This is limited to just linear.
class SolidProperties(object):
    def __init__(self, mat, Tgrid, epsil):
        self.props = sp.get_props(mat)
        self.epsilon = epsil
        self.pGrid = collections.defaultdict(dict)
        self.update_props(Tgrid)
        
    def update_props(self, Tgrid):
        for pt in Tgrid.keys():
            for prop in self.props.keys():
                self.pGrid[pt][prop] = np.interp(Tgrid[pt], self.props[prop][0, :], self.props[prop][1, :])
            
if __name__ == "__main__":
    import examples as ex
    print("You have chosen to run a predefined example: ")
    choice = bool(raw_input("Enter 1 for ziggurat, 0 for brick:  "))
    param = ex.Ziggurat() if choice else ex.Brick()

    ds = param.ds
    Nx, Ny, Nz = param.gridDim   #Number of grid points in each direction.
    Lx, Ly, Lz = param.LWH       #Full length of domain in each direction.
    #Grid points for plot.   
    Gx, Gy, Gz = np.meshgrid(np.arange(0,ds,Lx), 
                                np.arange(0,ds,Ly), 
                                    np.arange(0,ds,Lz))

    Tuno, fGrid = dict(), dict()
    xf, yf = Lx, Ly
    xi, yi = 0, 0
    
    Tuno, fGrid = make_grid(xi, xf, yi, yf, 0, param.T_init, zFlag=1)
    htSide = param.stepht * ds
    Aside = lambda xd, yd: 2.0*htside(xd*ds + yd*ds)
    surfaceArea = 0.0

    for z in range(1,Lz):
        if not param.thinning(z):
            surfaceArea += Aside(float(xf-xi), float(yf-yi))
            xi += 5 
            xf -= 5 
            yi += 5 
            yf -= 5
            
        Tuno, fGrid = make_grid(xi, xf, yi, yf, z, param.T_init)
    
    Tuno, fGrid = make_grid(xi, xf, yi, yf, Lz, param.T_init, zflag=2)
    surfaceArea += Aside(float(xf-xi), float(yf-yi))

    Tdos = copy.deepcopy(Tuno)





