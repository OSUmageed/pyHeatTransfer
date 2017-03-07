import os
import os.path as op
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import collections
import time
from mpl_toolkits.mplot3d import Axes3D
from deco import concurrent, synchronized

import geometry as geo
import SolidProp.PropertySI as sp
import convection as cv

thispath = op.abspath(op.dirname(__file__))
toK = 273.15

tag = geo.tags

def contourmaker(Tg, XX, yspot):
    npE = np.zeros_like(XX)
    for key in Tg.keys():
        x,y,z = key
        if y != yspot:
            continue
    
        npE[x,z] = Tg[key]

    return npE


def plotit(fg, ln, Tg, XX, ZZ, yspot, tn):

    TY = contourmaker(Tg, XX, yspot)
    fg.title("t = {:f.3} s".format(tn))
    ln.set_zdata(TY-toK)
    fg.canvas.draw()

#Doesn't do the ziggurat!
def make_grid(xi, xf, yi, yf, z, Ti, zFlag=""):

    xFlag = ["E", "W"]
    yFlag = ["S", "N"]
    typr = dict()
    Tmake = dict()

    #First x row
    gr = (xi, yi, z)
    typr[gr] = xFlag[0]+yFlag[0]+zFlag
    Tmake[gr] = Ti

    for y in range(yi+1,yf):
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

        for y in range(yi+1,yf):
            gr = (x, y, z)
            typr[gr] = zFlag
            Tmake[gr] = Ti

        gr = (x,yf,z)
        typr[gr] = yFlag[1]+zFlag
        Tmake[gr] = Ti

    #Last x row
    gr = (xf, yi, z)
    typr[gr] = xFlag[1]+yFlag[0]+zFlag
    Tmake[gr] = Ti

    for y in range(yi+1,yf):
        gr = (xf, y, z)
        typr[gr] = xFlag[1]+zFlag
        Tmake[gr] = Ti

    gr = (xf,yf,z)
    typr[gr] = xFlag[1]+yFlag[1]+zFlag
    Tmake[gr] = Ti
        
    return Tmake, typr
    

def step_forward(Tg_in, ky, Pg, typD, V, A, dt, ds, Ta, h, ep, qVol):
    ty = tag[typD]
    cond_coefficient = Pg['A']/(V*ds*ty['Vc'])

    cs = np.array(ky) + np.array(ty['Stencil'])
    ck = []
    for c in cs:
        ck.append(Tg_in[tuple(c)])

    conduction = cond_coefficient * (sum([ci*Ai*A for ci, Ai in list(zip(ty['Acond'],cs))]) - 
                Tg_in[ky]*sum(ty['Acond'])*A)

    cv_radiant = cv.ambientQ(Tg_in[ky], Ta, ty['Aconv'][0], h, ep)/(V*ty['Vc']*Pg['D']*Pg['CP'])
    
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
    def __init__(self, mat, Tgrid):
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
    choice = bool(int(input("Enter 1 for ziggurat, 0 for brick:  ")))
    param = ex.Ziggurat() if choice else ex.Brick()

    ds = param.ds
    Nx, Ny, Nz = param.gridDim   #Number of grid points in each direction.
    Lx, Ly, Lz = param.dims       #Full length of domain in each direction.
    #Grid points for plot.   
    Gx, Gy, Gz = np.meshgrid(np.arange(0,Lx+2.0*ds,ds), 
                                np.arange(0,Ly+2.0*ds,ds),
                                    np.arange(0,Lz+2.0*ds,ds))

    print(Gx.shape)

    Tuno, fGrid = dict(), dict()
    xf, yf = Nx, Ny
    xi, yi = 0, 0
    t = time.time()
    
    Tuno, fGrid = make_grid(xi, xf, yi, yf, 0, param.T_init, zFlag="B")
    t2 = time.time()
    print("First instantiation: {:.6f}s".format(t2-t))
    htSide = param.stepht * ds
    Aside = lambda xd, yd: 2.0*htSide*(xd*ds + yd*ds)
    surfaceArea = 0.0
    dt = param.dt

    for z in range(1,Nz):
        if not param.thinning(z):
            surfaceArea += Aside(float(xf-xi), float(yf-yi))
            xi += 5 
            xf -= 5 
            yi += 5 
            yf -= 5
         
        Tt, ft = make_grid(xi, xf, yi, yf, z, param.T_init)
        Tuno.update(Tt)
        fGrid.update(ft)
    
    Tt, ft = make_grid(xi, xf, yi, yf, Nz, param.T_init, zFlag="U")
    Tuno.update(Tt)
    fGrid.update(ft)
    
    surfaceArea += Aside(float(xf-xi), float(yf-yi))
    t3 = time.time()
    print("All instantiation: {:.6f}s".format(t3-t2))

    matProps = SolidProperties(param.mat, Tuno)
    tnow = 0.0
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    yval = 0.05
    Gsize = Gy.shape
    yplace = Gsize[1]//2
    Gxx = Gx[:, yplace, :]
    Gzz = Gz[:, yplace, :]
    Zv = contourmaker(Tuno, Gxx, yplace)
    
    lines = ax.plot_surface(Gxx, Gzz, Zv-toK)
    plt.show()
    print("here")
    t = [time.time()]
    while tnow < param.tfinal:
        Tdos = forward_call(Tuno, matProps.pGrid, fGrid, dt, ds, param.Ta, param.h, param.ep)
        matProps.update_props(Tdos)
        Tuno = forward_call(Tdos, matProps.pGrid, fGrid, dt, ds, param.Ta, param.h, param.ep)
        matProps.update_props(Tuno)
        tnow += dt*2.0
        t.append(time.time())
        print(t[-1]-t[-2])

        plotit(fig, lines, Tuno, Gxx, Gzz, yplace, tnow)


