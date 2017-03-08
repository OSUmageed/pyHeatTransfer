

toK = 273.15

shape_dict= { 
        'Brick': lambda z, ht: True
        'Ziggurat' : lambda z,ht: (z%ht)
}

class Thing(object):
        
    def __init__(self, mat, T_init, Ta, ep, dt, ds, h, qVol, tfinal, LWH, shape):
        self.mat = mat
        self.ds = ds
        self.dims = LWH
        self.gridDim = (int(d/self.ds)+1 for d in LWH) 
        self.dt = dt
        self.stepht = 
        self.T_init = T_init + toK
        self.Ta = Ta + toK
        self.h = h
        self.ep = ep
        self.qVol = qVol
        self.tfinal = tfinal
        self.thinning = shape_dict[shape]

zigg = Thing()
brick = Thing()

