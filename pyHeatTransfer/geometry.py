''' These are the global geometry parameters for the discretization.
It's ugly and it's hand written, but there's very little pattern in this madness.
Each coordinate will have a tag describing it's positionposition (i.e. center or top corner) in East, West, South, North, Up, Down (i.e. ESU would be a top corner at the 
origin of a specified line).
'''

from collections import defaultdict

''' Each tag refers to a dictionary with a stencil template, a coefficient for the node volume, the cross sectional area for each stencil point, and the surface area for ambient (convection and radiation) heat transfer which will be split up into vertical and horizontal components to allow free convection in the future.
'''

#At this moment we are ignoring inside corners.

A = [1]
B = [-1]
AB = A+B
f8 = 1.0/8.0
f4 = 1.0/4.0
f2 = 1.0/2.0
f1 = f2+f2
full = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]] 

tags = defaultdict(dict)

# CORNERS
# Outside top corners
loc = 'ESU'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,0,-1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4] 
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'ENU'
tags[loc]['Stencil'] = [[1,0,0], [0,-1,0], [0,0,-1]]  
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4] 
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'WNU'
tags[loc]['Stencil'] = [[-1,0,0],[0,-1,0],[0,0,-1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4]  
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'WSU'
tags[loc]['Stencil'] = [[-1,0,0],[0,1,0],[0,0,-1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4] 
tags[loc]['Aconv'] = [f2 + f4] 

#Outside bottom corners
loc = 'ESB'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,0,1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4]  
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'ENB'
tags[loc]['Stencil'] = [[1,0,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4]  
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'WNB'
tags[loc]['Stencil'] = [[-1,0,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4]  
tags[loc]['Aconv'] = [f2 + f4] 

loc = 'WSB'
tags[loc]['Stencil'] = [[-1,0,0], [0,1,0], [0,0,1]] 
tags[loc]['Vc'] = f8
tags[loc]['Acond'] = [f4, f4, f4]  
tags[loc]['Aconv'] = [f2 + f4] 

#EDGES
#----------------------------------------------
# Ouside vertical edges
loc = 'ES'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f2, f4, f4] 
tags[loc]['Aconv'] = [f1] 

loc = 'EN'
tags[loc]['Stencil'] = [[1,0,0], [0,-1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f2, f4, f4] 
tags[loc]['Aconv'] = [f1] 

loc = 'WN'
tags[loc]['Stencil'] = [[-1,0,0], [0,-1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f2, f4, f4] 
tags[loc]['Aconv'] = [f1] 

loc = 'WS'
tags[loc]['Stencil'] = [[-1,0,0], [0,1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f2, f4, f4] 
tags[loc]['Aconv'] = [f1] 

# Outside horizontal edges top
loc = 'EU'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,-1,0], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f4, f4, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'WU'
tags[loc]['Stencil'] = [[-1,0,0], [0,1,0], [0,-1,0], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f4, f4, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'NU'
tags[loc]['Stencil'] =[[1,0,0], [-1,0,0], [0,-1,0], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f4, f4, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'SU'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,1,0], [0,0,-1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f4, f4, f2, f2] 
tags[loc]['Aconv'] = [f1] 

# Outside horizontal edges bottom
loc = 'EB'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f4, f4, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'WB'
tags[loc]['Stencil'] = [[-1,0,0], [0,1,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f2, f4, f4, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'NB'
tags[loc]['Stencil'] =[[1,0,0], [-1,0,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f4, f4, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'SB'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,1,0], [0,0,1]] 
tags[loc]['Vc'] = f4
tags[loc]['Acond'] = [f4, f4, f2, f2] 
tags[loc]['Aconv'] = [f1] 

#FACES
#---------------------------------------------
#Faces cannot be inside or outside
loc = 'E'
tags[loc]['Stencil'] = [[1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f1, f2, f2, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'W'
tags[loc]['Stencil'] = [[-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f1, f2, f2, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'N'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,-1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f2, f2, f1, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'S'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,1,0], [0,0,1], [0,0,-1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f2, f2, f1, f2, f2] 
tags[loc]['Aconv'] = [f1] 

loc = 'U'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,-1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f2, f2, f2, f2, f1]  
tags[loc]['Aconv'] = [f1] 

loc = 'B'
tags[loc]['Stencil'] = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1]] 
tags[loc]['Vc'] = f2
tags[loc]['Acond'] = [f2, f2, f2, f2, f1]  
tags[loc]['Aconv'] = [f1] 

#The main one:  Center
loc = ""
tags[loc]['Stencil'] = full
tags[loc]['Vc'] = f1
tags[loc]['Acond'] = [f1]*6  
tags[loc]['Aconv'] = [0.0] 

#We alias full because the inside corners are also full stencils.  The main problem is recognizing those corners and edges.

#INSIDE (4 top and bottom corners, 4 top and bottom edges, ignore vertical inside corners)

#INSIDE CORNERS 
loc = "ESUI"
tags[loc]['Stencil'] = full #All inside items
tags[loc]['Vc'] = f2 + f8 #All inside corners 5 of 8 cubes in cube
tags[loc]['Acond'] = [f2+f4, f2, f2+f4, f2, f1, f4]
tags[loc]['Aconv'] = [f1+f4] 

loc = "ESBI"
tags[loc]['Stencil'] = full 
tags[loc]['Vc'] = f2 + f8 
tags[loc]['Acond'] = [f2+f4, f2, f2+f4, f2, f4, f1]
tags[loc]['Aconv'] = [f1+f4] 