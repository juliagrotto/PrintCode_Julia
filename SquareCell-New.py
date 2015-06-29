#battery-printer
#rely on home position set with 1st code loaded (separator)
#needs to re-zero "Z" between codes/syringes, but assume same x, y

#packaging bottom
#cathode
#separator
#packaging top
#anode
#sealing

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


#Define variables
printvel_LTO = 200	#printvel; mm/min
printvel_LFP = 160
printvel_pack = 55
printvel_sep = 90
printvel_seal = 55

tipsize_in = 1.54	#tipsize for electrodes, separator; mm
tipsize_out = 1.83	#tipsize for electrodes, separator; mm
tipsize_pack_in = 0.20 #tipsize for packaging; mm
tipsize_pack_out = 0.42 #tipsize for packaging; mm
tipsize_sep_in = 0.20 #tipsize for separator; mm
tipsize_sep_out = 0.42 #tipsize for aeparator; mm

square_edge = 20 #outer edge length in mm
square_thickness = 3 #outer edge to inner edge width in mm

offset_pack_in = square_thickness-tipsize_pack_out+(tipsize_pack_out-tipsize_pack_in)/2 #lower left corner
offset_pack_out = -(tipsize_pack_out-tipsize_pack_in)/2 #lower left corner

layers = 1    #layers for electrodes, separator; mm
layerheight =  0.5  #stepheight; mm  
layerheight_sep = 0.05
layers_pack = int((2*layers*layerheight+layerheight_sep)/tipsize_pack_in)+1
layerheight_pack = (2*layers*layerheight+layerheight_sep)/layers_pack
layerheight_seal = 0.1

port = 1
press_LFP = 40   #high pressure adaptor (1%KB LFP)
press_LTO = 40   #high pressure adaptor  (1.5%KB LTO)
press_pack = 70   #no high pressure adaptor
press_sep = 40   #no high pressure adaptor
press_seal = 70   #no high pressure adaptor

number_x= 1
number_y = 1
spacing_x = 5.0
spacing_y = 5.0


#Define function
def pressure_set (port, press):
    line = 'M9000 P{port} Q{press}'.format(port=port, press=press)
    g.write(line)

def pressure_on ():
    g.write('M9001')

def pressure_off ():
    g.write('M10000')

def square_3D (path_length, path_width, nozzle_size, z_step, layers): #starts lower outer left, starts at absolute Z=0
    
        step_number = int(path_width/nozzle_size) + 1
        
        step_size = path_width/step_number
        
        for i in range (layers):
            g.move(Z=z_step)
            pressure_on()
            
            for i in range (step_number-1):
                g.move(x=path_length-nozzle_size-i*2*step_size)
                g.move(y=path_length-nozzle_size-i*2*step_size)
                g.move(x=-(path_length-nozzle_size-i*2*step_size))
                g.move(y=-(path_length-nozzle_size-i*2*step_size))
                g.move(x=step_size, y=step_size) 
                
            g.move(x=path_length-nozzle_size-(step_number-1)*2*step_size)
            g.move(y=path_length-nozzle_size-(step_number-1)*2*step_size)
            g.move(x=-(path_length-nozzle_size-(step_number-1)*2*step_size))
            g.move(y=-(path_length-nozzle_size-(step_number-1)*2*step_size))
            
            pressure_off()
            g.dwell(3)
            g.move(x=-step_size*(step_number-1), y=-step_size*(step_number-1))
                                                            
  
#file- 1packaging
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/squarecell/squarecell_20mm_3mm_1packaging.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(x=0,y=0,Z=0) #lower left corner, nozzle edge with substrate edge, absolute zero
g.feed(printvel_pack)
g.abs_move(Z=layerheight_pack)
g.abs_move(x=offset_pack_in, y=offset_pack_in, )
pressure_set(port, press_pack)
pressure_on()
        
for i in range(layers_pack):
    g.rect(square_edge-2*square_thickness+tipsize_pack_in, square_edge-2*square_thickness+tipsize_pack_in, direction='CCW', start='LL')
    g.move(Z=layerheight_pack)
        
pressure_off()
g.dwell(3.0)

g.move(x=2,y=2)
g.abs_move(Z=5)
                
g.abs_move(x=offset_pack_out, y=offset_pack_out)
g.abs_move(Z=layerheight_pack)
pressure_set(port, press_pack)
pressure_on()
        
for i in range(layers_pack):
    g.rect(square_edge-tipsize_pack_in, square_edge-tipsize_pack_in, direction='CCW', start='LL')
    g.move(Z=layerheight_pack)
        
pressure_off()
g.dwell(3.0)
  
g.move(x=-2, y=-2)

#file - 2cathode
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/squarecell/squarecell_20mm_3mm_2cathode.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )


#Code starts
g.set_home(Z=0)
g.feed(printvel_LFP)
g.abs_move(Z=5)
g.abs_move(x=tipsize_pack_in+tipsize_out, y=tipsize_pack_in+tipsize_out)
g.abs_move(Z=0)
pressure_set(port, press_LFP)       
square_3D (square_edge-2*tipsize_pack_in, square_thickness-2*tipsize_pack_in, tipsize_out, layerheight, layers)
g.abs_move(Z=5)
        

#file - 3separator
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/squarecell/squarecell_20mm_3mm_3separator.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(Z=0)
g.feed(printvel_sep)
g.abs_move(Z=5)
g.abs_move(x=tipsize_sep_in+tipsize_pack_out, y=tipsize_sep_in+tipsize_pack_out)
g.abs_move(Z=layers*layerheight)
pressure_set(port, press_sep)       
square_3D (square_edge-2*tipsize_sep_in, square_thickness-2*tipsize_sep_in, tipsize_sep_out, layerheight_sep, 1)
g.abs_move(Z=5)       

#file - 4anode
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/squarecell/squarecell_20mm_3mm_4anode.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(Z=0)
g.feed(printvel_LTO)
g.abs_move(Z=5)
g.abs_move(x=tipsize_pack_in+tipsize_out, y=tipsize_pack_in+tipsize_out)
g.abs_move(Z=layers*layerheight+layerheight_sep)
pressure_set(port, press_LTO)       
square_3D (square_edge-2*tipsize_pack_in, square_thickness-2*tipsize_pack_in, tipsize_out, layerheight, layers)
g.abs_move(Z=5)


#file- 5seal
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/squarecell/squarecell_20mm_3mm_5seal.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(Z=0)
g.abs_move(Z=5)#lower left corner, nozzle edge with substrate edge, absolute zero
g.feed(printvel_pack)
g.abs_move(x=offset_pack_in, y=offset_pack_in)
g.abs_move(Z=2*layers*layerheight+layerheight_sep+layerheight_seal)
pressure_set(port, press_pack)
pressure_on()        

g.rect(square_edge-2*square_thickness+tipsize_pack_in, square_edge-2*square_thickness+tipsize_pack_in, direction='CCW', start='LL')
       
pressure_off()
g.dwell(3.0)

g.abs_move(Z=5)
                
g.abs_move(x=offset_pack_out, y=offset_pack_out)
g.abs_move(Z=2*layers*layerheight+layerheight_sep+layerheight_seal)
pressure_set(port, press_pack)
pressure_on()
        
g.rect(square_edge-tipsize_pack_in, square_edge-tipsize_pack_in, direction='CCW', start='LL')
        
pressure_off()
g.dwell(3.0)
   
g.abs_move(Z=5)

       
               
#To end
#g.view(backend='matplotlib')
#g.view()
g.teardown()