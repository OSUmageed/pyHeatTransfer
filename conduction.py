import os
import os.path as op
import sys
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import collections
from deco import concurrent, synchronized

import geometry as geo
import SolidProp.PropertySI as sp
import convection as cv

thispath = op.abspath(op.dirname(__file__))
toK = 273.15

tag = geo.tags

def plotit(ax, XX, YY, npE, zPlane, dt):
    npE = np.zeros_like(XX)
    for key in Tg.keys():
        x,y,z = key
        if z != zPlane:
            continue

        npE[x,y] = Tg[key]

    ax.draw(XX,YY, npE)

#Doesn't do the ziggurat!
def make_grid(xi, xf, yi, yf, z, Ti, zFlag=""):

    xFlag = ["E", "W"]
    yFlag = ["S", "N"]
    typr = dict()
    Tmake = dict()

    #First x row
    gr = (xi, yi, z)
    typr[gr]] = xFlag[0]+yFlag[0]+zFlag
    Tmake[gr] = Ti

    for y in range(yi+1,yf)
        gr = (xi, y, z)
        typr[gr] = xFlag[0]+zFlag
        Tmake[gr] = Ti

    gr = (xi, yf, z)
    typr[gr] = xFlag[0]+yFlag[1]+zFlag
    Tmake[gr] = Ti

    # All central x rows
    for x in range(xi+1,xf):
        gr = (x, yi, z)
        typr[gr] = yFlag[0]+zFlag
        Tmake[gr] = Ti

        for y in range(yi+1,yf)
            gr = (x, y, z)
            typr[gr] = zFlag
            Tmake[gr] = Ti

        gr = [(x,yf,z)]
        typr[gr] = yFlag[1]+zFlag
        Tmake[gr] = Ti

    #Last x row
    gr = (xf, yi, z)
    typr[gr]] = xFlag[1]+yFlag[0]+zFlag
    Tmake[gr] = Ti

    for y in range(yi+1,yf)
        gr = (xf, y, z)
        typr[gr] = xFlag[1]+zFlag
        Tmake[gr] = Ti

    gr = (xf,yf,z)
    typr[gr] = xFlag[1]+yFlag[1]+zFlag
    Tmake[gr] = Ti
        
    return Tmake, typr
    

@concurrent
def step_forward((Tg_in, key, Pg, typD, qVol, dt, ds):
    ty = tag[typD[key]]
    stH = list(key)
    #Probably one big list comprehension
    for i, st in enumerate(ty['Stencil'])
        for ii, s in enumerate(st):
            stencil = list(key)

        
@synchronized
def forward_call(Tg_in, Tg_out, Pg, typD, qVol, dt, ds):
    
    for key in Tg_in.keys():
        Tg_out[key] = step_forward(Tg_in, key, Pg, typD, qVol, dt, ds):

    return Tg_out

#could use scipy interpolate to do a spline.  This is limited to just linear.
class SolidProperties(object):
    def __init__(self, mat, Tgrid, epsil):
        self.props = sp.get_props(mat)
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
    
    Tuno, fGrid = make_grid(xi, xf, yi, yf, 0, param.T_init, zFlag="B")
    htSide = param.stepht * ds
    Aside = lambda xd, yd: 2.0*htside(xd*ds + yd*ds)
    surfaceArea = 0.0
    dt = param.dt

    for z in range(1,Lz):
        if not param.thinning(z):
            surfaceArea += Aside(float(xf-xi), float(yf-yi))
            xi += 5 
            xf -= 5 
            yi += 5 
            yf -= 5
            
        Tt, ft = make_grid(xi, xf, yi, yf, z, param.T_init)
        Tuno.update(Tt)
        fGrid.update(ft)
    
    Tt, ft = make_grid(xi, xf, yi, yf, Lz, param.T_init, zFlag="U")
    Tuno.update(Tt)
    fGrid.update(ft)

    surfaceArea += Aside(float(xf-xi), float(yf-yi))

    Tdos = copy.deepcopy(Tuno)

    matProps = SolidProperties(mat, Tuno)
    tnow = 0.0

    while tnow < tfinal:
        Tdos = forward_call(Tuno, Tdos, Pg, fGrid, param.qVol, param.dt, param.ds)
        matprops.update_props(Tdos)
        Tuno = forward_call(Tdos, Tuno, Pg, fGrid, param.qVol, param.dt, param.ds)
        matprops.update_props(Tuno)
        tnow += dt

        #Do plotting





