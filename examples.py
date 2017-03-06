
toK = 273.15

class Ziggurat(object):
    def __init__(self, mat='Aluminum', T_init=25.0, 
                Ta=500.0, ep=0.077,
                LWH=(0.1,0.1,1.0)):

        self.mat = mat
        self.ds = 0.001
        self.dims = LWH
        self.gridDim = (int(d/ds)+1 for d in LWH) 
        self.dt = 0.001
        self.stepht = 20
        self.T_init = T_init + toK
        self.Ta = Ta + toK
        self.h = 10.0
        self.ep = ep
        self.thinning = lambda z: (z%self.stepht) 

class Brick(object):
    def __init__(self, mat='Aluminum', T_init=25.0, 
                Ta=500.0, ep=0.077,
                LWH=(0.1,0.1,1.0)):

        self.mat = mat
        self.ds = 0.001
        self.dims = LWH
        self.gridDim = (int(d/ds)+1 for d in LWH) 
        self.dt = 0.001
        self.stepht = LWH[-1]
        self.T_init = T_init + toK
        self.Ta = Ta + toK
        self.h = 10.0
        self.ep = ep
        self.thinning = lambda z: True
