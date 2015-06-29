#battery-printer
#needs to re-zero "Z" between codes/syringes, but assume same x, y

#horizontal_serpentine_layer_1
#vertical_serpentine_layer_2

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
printvel = 4 #printvel; mm/s
printlength = 20 #in mm

LED_contact = 0.2 #in mm
LED_width = 0.8 #in mm
LED_length = 1.6 #in mm
LED_length_excluding_contacts = LED_length - (2*LED_contact) #in mm
LED_pathgap = 0.2 #in mm
number_of_meanders = 1
tipsize_in = 0.2  #tipsize for electrodes, separator; mm
tipsize_out = 0.42  #tipsize for electrodes, separator; mm

#variables that control s (VOLTAGE PARALLEL MUST BE LESS THAN VLTSRC/NUMLED)
Vltp = 3.14 #Voltage parallel to LED
SrcVlt = 25 #Source Voltage
numLED = 6 #total number of LED 
l = 20 #the length of the long path in mm must be greater than print_structure_length
a = 0.2 #between LED pathgap in mm
Rb = 91.65*(l + 2*a)/3.148 #Resistance between LEDs
Rp = (Vltp/SrcVlt)*(Rb*(numLED-1))/(1-(Vltp/SrcVlt*numLED))
s = ((Rp*3.148/91.65) - (2*l) +0.8)/2 #the length of the short path in mm


layers = 1    #layers for electrodes, separator; mm
z_step =  0.18  #layerheight; mm  

port = 4
press = 45

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

def serpentine_vertical (LED_pathgap, a, tipsize_in, LED_width, z_step, layers, l, s): #starts lower outer left, starts at absolute Z=0
        
        pressure_on()
        for i in range (numLED/2):
            g.move(x=a+tipsize_in)
            g.move(y=l)
            
            for i in range (number_of_meanders):
                g.move(x=LED_pathgap+tipsize_in)
                g.move(y=-s)
                g.move(x=LED_pathgap+tipsize_in) 
                g.move(y=s)
                
            g.move(x=LED_pathgap+tipsize_in)
            g.move(y=-l)
            g.move(x=a+tipsize_in)
            g.move(y=l)
            
            for i in range (number_of_meanders):
                g.move(x=LED_pathgap+tipsize_in)
                g.move(y=+s)
                g.move(x=LED_pathgap+tipsize_in) 
                g.move(y=-s)
                
            g.move(x=LED_pathgap+tipsize_in)
            g.move(y=+l)
            g.move(x=a+tipsize_in)
            g.move(y=-l)
            
        pressure_off()
        g.dwell(3)
                                                            
def serpentine_horizontal (LED_pathgap, a, tipsize_in, LED_width, z_step, layers, l, s): #starts lower outer left, starts at absolute Z=0
    
        pressure_on()
        for i in range (numLED/2):
            g.move(y=a+tipsize_in)
            g.move(x=l)
            
            for i in range (number_of_meanders):
                g.move(y=LED_pathgap+tipsize_in)
                g.move(x=-s)
                g.move(y=LED_pathgap+tipsize_in) 
                g.move(x=s)
                
            g.move(y=LED_pathgap+tipsize_in)
            g.move(x=-l)
            g.move(y=a+tipsize_in)
            g.move(x=l)
            
            for i in range (number_of_meanders):
                g.move(y=LED_pathgap+tipsize_in)
                g.move(x=+s)
                g.move(y=LED_pathgap+tipsize_in) 
                g.move(x=-s)
                
            g.move(y=LED_pathgap+tipsize_in)
            g.move(x=+l)
            g.move(y=a+tipsize_in)
            g.move(x=-l)
            
        pressure_off()
        g.dwell(3)
                                                                    
#file- singlelayer
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/serpentine/vltpserpentine_singlelayer.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(x=0,y=0,Z=0) #lower left corner, nozzle edge with substrate edge, absolute zero
g.feed(printvel)
g.abs_move(Z=z_step)
g.abs_move(X=LED_width + (2*tipsize_in))
pressure_set(port, press)
serpentine_vertical (LED_pathgap, a, tipsize_in, LED_width, z_step, layers, l, s)

#file- doublelayer
g = G(
        outfile = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/serpentine/vltpserpentine_doublelayer.txt",
        header = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/header_batteryprinter.txt",
        footer = "/Users/juliagrotto/Documents/Github/PrintCode_Julia/footer_batteryprinter.txt",
        aerotech_include = False,
        direct_write = False,
        print_lines = False, 
        )

#Code starts
g.set_home(x=0,y=0,Z=0) #lower left corner, nozzle edge with substrate edge, absolute zero
g.feed(printvel)
g.abs_move(Z=z_step)
g.abs_move(X=LED_width + (2*tipsize_in))
pressure_set(port, press)
serpentine_vertical (LED_pathgap, a, tipsize_in, LED_width, z_step, layers, l, s) 
g.move(Z=z_step)  
g.abs_move(X=0,Y=(LED_width + (2*tipsize_in)))
pressure_set(port, press)     
serpentine_horizontal (LED_pathgap, a, tipsize_in, LED_width, z_step, layers, l, s) 

#To end
#g.view(backend='matplotlib')
#g.view()
g.teardown()