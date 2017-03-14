#I suppose the idea is that it gets these values from somewhere and takes off.
#Regardless of where those values come from.

import os
import os.path as op
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import collections
import time
import random
from deco import concurrent, synchronized

sourcepath = op.abspath(op.dirname(__file__))
gitpath = op.dirname(sourcepath) #Top level of git repo
os.chdir(sourcepath)
sys.path.append(gitpath)

import geometry as geo
import SolidProp.PropertySI as sp
import convection as cv

shape_func = { 
        'Brick': lambda z, ht: True,
        'Ziggurat' : lambda z, ht: (z%ht)
}

thispath = op.abspath(op.dirname(__file__))
toK = 273.15

tag = geo.tags

def contourmaker(Tg, XX, yspot):
    npE = np.zeros_like(XX)
    for key in Tg.keys():
        x,y,z = key
        if y != yspot:
            continue
                
        npE[z,x] = Tg[key]

    return npE

def randT(T):
    return 0.1*random.random() + T

#Doesn't do the ziggurat!
def make_grid(xi, xf, yi, yf, z, Ti, zFlag=""):

    xFlag = ["E", "W"]
    yFlag = ["S", "N"]
    typr = dict()
    Tmake = dict()

    #First x row
    gr = (xi, yi, z)
    typr[gr] = xFlag[0]+yFlag[0]+zFlag
    Tmake[gr] = randT(Ti)

    for y in range(yi+1,yf):
        gr = (xi, y, z)
        typr[gr] = xFlag[0]+zFlag
        Tmake[gr] = randT(Ti)

    gr = (xi, yf, z)
    typr[gr] = xFlag[0]+yFlag[1]+zFlag
    Tmake[gr] = randT(Ti)

    # All central x rows
    for x in range(xi+1,xf):
        gr = (x, yi, z)
        typr[gr] = yFlag[0]+zFlag
        Tmake[gr] = randT(Ti)

        for y in range(yi+1,yf):
            gr = (x, y, z)
            typr[gr] = zFlag
            Tmake[gr] = randT(Ti)

        gr = (x,yf,z)
        typr[gr] = yFlag[1]+zFlag
        Tmake[gr] = randT(Ti)

    #Last x row
    gr = (xf, yi, z)
    typr[gr] = xFlag[1]+yFlag[0]+zFlag
    Tmake[gr] = randT(Ti)

    for y in range(yi+1,yf):
        gr = (xf, y, z)
        typr[gr] = xFlag[1]+zFlag
        Tmake[gr] = randT(Ti)

    gr = (xf,yf,z)
    typr[gr] = xFlag[1]+yFlag[1]+zFlag
    Tmake[gr] = randT(Ti)
        
    return Tmake, typr

def step_forward(Tg_in, ky, Pg, typD, V, A, dt, ds, Ta, h, ep, qVol):
    ty = tag[typD]
    cond_coefficient = Pg['A']/(V*ds*ty['Vc'])

    cs = np.array(ky) + np.array(ty['Stencil'])
    ck = []
    for c in cs:
        ck.append(Tg_in[tuple(c)])

    conduction = cond_coefficient * (sum([ci*Ai*A for ci, Ai in list(zip(ty['Acond'],ck))]) - 
                Tg_in[ky]*A*sum(ty['Acond']))

    cv_radiant = cv.ambientQ(Tg_in[ky], Ta, ty['Aconv'][0]*A, h, ep)/(V*ty['Vc']*Pg['D']*Pg['CP'])
    
    return Tg_in[ky] + dt*(conduction + cv_radiant + qVol/Pg['D']*Pg['CP'])


def forward_call(Tg_in, Pg, typD, dt, ds, Ta, h, ep, qVol=0.0):
    A = ds**2
    V = A*ds 
    Tg_out = dict()
    for key in Tg_in.keys():
        Tg_out[key] = step_forward(Tg_in, key, Pg[key], typD[key], V, 
                        A, dt, ds, Ta, h, ep, qVol)

    return Tg_out

#could use scipy interpolate to do a spline.  This is limited to just linear.
class SolidProperties(object):
    def __init__(self, mat, Tgrid={}):
        self.props = sp.get_props(mat)
        self.pGrid = collections.defaultdict(dict)
        self.update_props(Tgrid)
        
    #Should accommodate lists in order to 
    def update_props(self, Tgrid):
        for pt in Tgrid.keys():
            for prop in self.props.keys():
                self.pGrid[pt][prop] = np.interp(Tgrid[pt], self.props[prop][0, :], self.props[prop][1, :])
            
    def query_props(self, Temp):
        Tget = Temp if isinstance(Temp, list) else [Temp]
        out = collections.defaultdict(dict)
        for T in Tget:
            for prop in self.props.keys():
                out[T][prop] = np.interp(T, self.props[prop][0, :], self.props[prop][1, :])

        return out

#Hmm doesn't quite work need T before 
class HeatSimulation(object):
    def __init__(self, specificDict):
        self.parameter_dict = specificDict
        self.mat = specificDict['mat']
        self.ds = specificDict['ds']
        self.dt = specificDict['dt']
        self.Ti = specificDict['Ti'] + toK
        self.Ta = specificDict['Ta'] + toK
        self.h = specificDict['h']
        self.ep = specificDict['ep']
        self.Lx = specificDict['Lx'] 
        self.Ly = specificDict['Ly'] 
        self.Lz = specificDict['Lz'] 
        self.tF = specificDict['tFinal']
        self.tNow = 0.0 
        self.Nx = int(Lx/ds)+1 
        self.Ny = int(Ly/ds)+1 
        self.Nz = int(Lz/ds)+1
        self.Gx, self.Gz = np.meshgrid(np.arange(0,Lx+2.0*ds,ds), np.arange(0,Lz+2.0*ds,ds))
        self.Tuno, self.fGrid = self.make_grid()
        self.matProps = SolidProperties(self.mat, self.Tuno)

    def make_grid(self):
        return 0, 0
    

def initialize(specificDict):
    ds = specificDict['ds']
    Lx, Ly, Lz = specificDict['Lx'], specificDict['Ly'], specificDict['Lz'] 
    Nx, Ny, Nz = int(Lx/ds)+1, int(Ly/ds)+1, int(Lz/ds)+1
    Gx, Gz = np.meshgrid(np.arange(0,Lx+2.0*ds,ds), np.arange(0,Lz+2.0*ds,ds))

    dt = specificDict['dt']
    Ti = specificDict['Ti'] + toK
    Ta, h, ep = specificDict['Ta'] + toK, specificDict['h'], specificDict['ep']
    xf, yf = Nx, Ny
    xi, yi = 0, 0
    Tuno, fGrid = make_grid(xi, xf, yi, yf, 0, Ti, zFlag="B")

    cD = specificDict['stepD']
    stepFunction = shape_func[specificDict['shape']]

    for z in range(1,Nz):
        if not stepFunction(z, specificDict['stepH']):
            xi += cD
            xf -= cD
            yi += cD
            yf -= cD
            
        Tt, ft = make_grid(xi, xf, yi, yf, z, Ti)
        Tuno.update(Tt)
        fGrid.update(ft)
    
    Tt, ft = make_grid(xi, xf, yi, yf, Nz, Ti, zFlag="U")
    Tuno.update(Tt)
    fGrid.update(ft)

    tnow = 0.0
    yval = Ly/2
    Gsize = Gx.shape
    yplace = Gsize[1]//2
        
    matProps = SolidProperties(specificDict['mat'], Tuno)
    t = [time.time()]
    print(Gsize, len(Tuno.keys()))


    while tnow < specificDict['tFinal']:
        Tdos = forward_call(Tuno, matProps.pGrid, fGrid, dt, ds, Ta, h, ep)
        matProps.update_props(Tdos)
        Tuno = forward_call(Tdos, matProps.pGrid, fGrid, dt, ds, Ta, h, ep)

        matProps.update_props(Tuno)

        tnow += dt*2.0
        t.append(time.time())
        print(tnow, t[-1]-t[-2])

    Zv = contourmaker(Tuno, Gx, yplace)
    CS = plt.contour(Gx, Gz, Zv-toK, 5)
    plt.title("yaxis = {:.3f}, t = {:.3f} s".format(yval, tnow))
    plt.ylabel('Z axis')
    plt.xlabel('X axis')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.grid(True)
    plt.show()

    return 'Yay'

if __name__ == "__main__":

    import examples as ex
    print("You have chosen to run a predefined example: ")
    choice = bool(int(input("Enter 1 for ziggurat, 0 for brick:  ")))

    param = ex.zigg if choice else ex.bricky
    initialize(param)