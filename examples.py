import copy

zigg = {'Ti': 25.0,
        'Ta': 500.0,
        'mat': 'Aluminum',
        'dt': 0.01,
        'ds': 0.01,
        'Lx': 0.2,
        'Ly': 0.2,
        'Lz': 0.5,
        'h': 10,
        'ep': 0.75,
        'qVol': 0.0,
        'tFinal': 50.0,
        'stepH': 20,
        'stepD': 5,
        'shape': 'Ziggurat'
}

bricky = copy.deepcopy(zigg)

bricky['shape'] = 'Brick'

