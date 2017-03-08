import os
import os.path as op
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import SolidProp as solid

g = 9.81

def ambientQ(T, Ta, A, h, ep):
    sig = 5.67e-8
    return (h*A*np.abs(T-Ta) + ep*sig*A*np.abs(T**4-Ta**4))

def colebrook(Re, e, D, f):
    g = e/(D*3.7) + 2.51/(Re*np.sqrt(f))
    fn = -1.0/(2.0*np.log10(g)) 
    if np.isclose(np.abs(fn-f) < tol):
        return colebrook(Re, e, D, fn) 
    else:
        return fn

class Fluid(object):
    def __init__(self, Tref, Pref, media):
        self.Tref = Tref
        self.Pref = Pref
        self.media = media
        self.k = cp.PropsSI('L', 'P', Pref, 'T', Tref, media) 
        self.Cp = cp.PropsSI('C', 'P', Pref, 'T', Tref, media) 
        self.rho = cp.PropsSI('D', 'P', Pref, 'T', Tref, media) 
        self.muu = cp.PropsSI('V', 'P', Pref, 'T', Tref, media) 
        self.nuu = self.rho/self.muu     
        self.Pr = cp.PropsSI('Pr', 'P', Pref, 'T', Tref, media) 


class Forced(Fluid):
    pass

class Free(Fluid): 
    pass
