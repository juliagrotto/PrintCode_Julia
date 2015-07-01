#minicaster
#needs to re-zero "Z" between codes/syringes, but assume same x, y

from mecode import G

#nordson Tips sizes (color, inner diameter, outer diamter, in mm)   
#Olive 1.54 1.83
#Amber 1.36 1.65
#Grey 1.19 ??
#Green 0.84 1.27
#Pink 0.61 0.91
#Purple 0.51 0.82
#Blue 0.41 0.72
#Orange 0.33 0.65
#Red 0.25 0.52
#Clear 0.20 0.42
#Lavender 0.15 0.31
#Yellow 0.10 0.24


#Define Independant Variables

printvel = 4	#printvel; mm/s
tipsize_in = 0.2  #tipsize for electrodes, separator; mm
tipsize_out = 0.42  #tipsize for electrodes, separator; mm
square_side_length = 2 #length in mm

offset = 1 #1=on 0=off  (if on the grid will have 2 less lines)
collumn_height = 30 #in mm
grid_lines = 6 #must be even number

#Dependant Variables
path_gap = (square_side_length - (grid_lines*tipsize_in))/(grid_lines - 1) #distance between successive lines in mm
offset_dist = (path_gap + tipsize_in)/2 #in mm
layers = int(collumn_height/(tipsize_in*0.8))   #number of layers in collumn ; int
z_step =  tipsize_in*0.8  #layerheight 80% of nozzel inner diameter ; mm  
num_of_S_structures = ((grid_lines/2) - 1)
quadruple_layers = int(layers/4) #number of vertical, horizontal,vertical(offset), horizontal(offset) blocks
remainder_layers = layers - (quadruple_layers*4)

port = 4
press = 45

number_x= 1
number_y = 1
spacing_x = 5.0
spacing_y = 5.0


#Define function
def pressure_set (port, press):
    line = 'Call setPress P{port} Q{press}'.format(port=port, press=press)
    g.write(line)

def pressure_toggle (port):
    line = 'togglePress P{port}'.format(port=port)
    g.write(line)

def collumn_grid (path_gap, quadruple_layers, num_of_S_structures, square_side_length, tipsize_in, z_step, layers, offset_dist, offset): #starts upper left, starts at absolute X=0, Y=0, Z=0
        
        pressure_toggle(port)
        
        for i in range (quadruple_layers):
            
            for i in range (num_of_S_structures):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures):
                g.move(x=square_side_length)
                g.move(y=path_gap+tipsize_in)
                g.move(x=-square_side_length) 
                g.move(y=path_gap+tipsize_in)
                
            g.move(x=square_side_length)
            g.move(y=path_gap+tipsize_in)
            g.move(x=-square_side_length)
            
            pressure_toggle(port)
            g.move(z=z_step)
            g.abs_move(X=0, Y=0)
            g.move(x=offset_dist*offset)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures - (1*offset)):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            g.move(y=offset_dist*offset)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures - (1*offset)):
                g.move(x=square_side_length)
                g.move(y=path_gap+tipsize_in)
                g.move(x=-square_side_length) 
                g.move(y=path_gap+tipsize_in)
                
            g.move(x=square_side_length)
            g.move(y=path_gap+tipsize_in)
            g.move(x=-square_side_length)
            
            pressure_toggle(port)
            g.move(z=z_step)
            g.abs_move(X=0, Y=0)
            pressure_toggle(port)
        
        if remainder_layers == '3':
            
            for i in range (num_of_S_structures):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures):
                g.move(x=square_side_length)
                g.move(y=path_gap+tipsize_in)
                g.move(x=-square_side_length) 
                g.move(y=path_gap+tipsize_in)
                
            g.move(x=square_side_length)
            g.move(y=path_gap+tipsize_in)
            g.move(x=-square_side_length)
            
            pressure_toggle(port)
            g.move(z=z_step)
            g.abs_move(X=0, Y=0)
            g.move(x=offset_dist*offset)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures - (1*offset)):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            g.move(y=offset_dist*offset)
            pressure_toggle(port)
            
        if remainder_layers == '2':
            
            for i in range (num_of_S_structures):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            pressure_toggle(port)
            
            for i in range (num_of_S_structures):
                g.move(x=square_side_length)
                g.move(y=path_gap+tipsize_in)
                g.move(x=-square_side_length) 
                g.move(y=path_gap+tipsize_in)
                
            g.move(x=square_side_length)
            g.move(y=path_gap+tipsize_in)
            g.move(x=-square_side_length)
            
            pressure_toggle(port)
            g.move(z=z_step)
            g.abs_move(X=0, Y=0)
            g.move(x=offset_dist*offset)
            pressure_toggle(port)
        
        if remainder_layers == '1':
            
            for i in range (num_of_S_structures):
                g.move(y=square_side_length)
                g.move(x=path_gap+tipsize_in)
                g.move(y=-square_side_length) 
                g.move(x=path_gap+tipsize_in)
                
            g.move(y=square_side_length)
            g.move(x=path_gap+tipsize_in)
            g.move(y=-square_side_length)
            
            pressure_toggle(port)
            g.move(z_step)
            g.abs_move(X=0, Y=0)
            pressure_toggle(port)
            
        pressure_toggle(port)
        g.dwell(3)
                                                            
                                           
#CCmesh
g = G(
        outfile ="/Users/juliagrotto/Documents/Github/PrintCode_Julia/CCmesh/CCmesh.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(x=0,y=0,Z=0) #lower left corner, nozzle edge with substrate edge, absolute zero
g.feed(printvel)
g.abs_move(Z=z_step)
pressure_set(port, press)
collumn_grid (path_gap, quadruple_layers, num_of_S_structures, square_side_length, tipsize_in, z_step, layers, offset_dist, offset)


#To end
#g.view(backend='matplotlib')
#g.view()
g.teardown()