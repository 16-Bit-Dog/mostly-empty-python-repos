import numpy as np   
import PIL #meh, I'll import all for now
import pygame
import tkinter as tk
from tkinter import filedialog
from matplotlib import image
from matplotlib import pyplot
#from matplotlib.pyplot import ion
import time

pygame.init()
pyplot.axis('off')
pyplot.grid(b=None)
pyplot.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

pyplot.gca().set_axis_off()

pyplot.margins(0,0)
pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())

#pyplot.savefig("fileOut.PNG", bbox_inches = 'tight', pad_inches = 0)
pyplot.savefig("fileOut.PNG", format='png', transparent=True, dpi=300, pad_inches = 0)
#ion()
WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
 
FONT = pygame.font.SysFont('timesnewroman',  30)

class pygameLogic:
    def __init__(self):
        self.background_colour = (255,255,255,0)
        self.run = 1

        self.FilterMode = -1

        self.B1 = FONT.render('L-Fringe', True, GREEN, BLUE)
        self.B2 = FONT.render('H-Dark', True, GREEN, BLUE)
        self.B3 = FONT.render('S-Light', True, GREEN, BLUE)
        self.B4 = FONT.render('Text', True, GREEN, BLUE)
        self.B5 = FONT.render('Text', True, GREEN, BLUE)

        self.D1 = FONT.render('Pop Up windows show the Before and After', True, GREEN, (0,0,0,0))
        self.D2 = FONT.render('You can also save; click the cartridge button!', True, GREEN, (0,0,0,0))

        self.pos = (0,0)

        self.NeedImage = 0 # start image loader as false
        self.FileChosen = ""
        self.imageData = list()
        self.ShowBool = 0
        self.tick = 0 #used for delay to allow pygame to have time to finish draw call to screen... did not find a way to check if a draw call is in progress, so I just chosen to tick 10 frames - since then I will be safe for most hardware
   
    def FilterBrightFrizz(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        

        #data = np.fromstring(self.imageData[0].tostring_rgb(), dtype=np.uint8, sep='') #forces to RGB... don't think I care... who needs alpha any ways ... but I will still work around alpha in areas in case it remotely matters... not like I need to over eng stuff
        #data = data.reshape(self.imageData[0].get_width_height()[::-1] + (3,))

        #self.imageData.append(data)

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                 #r,g,b,a <-- alpha may not be present, if using you MUST check for alpha - also always modify in such a way that it is safe for alph and non alpha containing images
                #YOU MUST CAST ALL VALUES TO AN INT else they are a u8 --> 8 bits is going to overflow and not work as intended
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) > 300):
                    arr = np.array([self.imageData[1][i][ii][0]*1.2, self.imageData[1][i][ii][1]*1.2, self.imageData[1][i][ii][2]*1.2])
                    self.imageData[1][i][ii] = arr
                    #refrence y and then x axis

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self
    def SelectButton(self):
        #choose a button to filter with

        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, self.B1.get_height()) )
        pygame.draw.rect(screen, RED, (140, 0, 10, HEIGHT) ) 
        pygame.draw.rect(screen, RED, (290, 0, 10, HEIGHT) ) 
        pygame.draw.rect(screen, RED, (440, 0, 10, HEIGHT) ) 
        
        pygame.draw.rect(screen, RED, (0, self.B1.get_height(), WIDTH, 5) ) 
        


        screen.blit(self.B1, (0,0))

        screen.blit(self.B2, (150,0))
        
        screen.blit(self.B3, (300,0))

        screen.blit(self.B4, (450,0))


        if(pygame.mouse.get_pressed()[0] == 1): # indes 0 is left click - true means clicked
            if (pygame.mouse.get_pos()[1] > 0 and pygame.mouse.get_pos()[1] < self.B1.get_height()):
                if (pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[0] < 140):#I did not normalize these points to allow fine tuning if needed - plus this way iamges can be added easily 
                    self.FilterMode = 0
                elif (pygame.mouse.get_pos()[0] > 150 and pygame.mouse.get_pos()[0] < 290 + self.B2.get_width()):
                    self.FilterMode = 1
                elif (pygame.mouse.get_pos()[0] > 350 and pygame.mouse.get_pos()[0] < 440 + self.B3.get_width()):
                    self.FilterMode = 2
                elif (pygame.mouse.get_pos()[0] > 450 and pygame.mouse.get_pos()[0] < 590 + self.B4.get_width()):
                    self.FilterMode = 3

        return self
    
    def SelectImage(self):
        root = tk.Tk()
        root.withdraw()
        
        NotDone  = 1

        files = filedialog.askopenfilenames() #Not fully pausing runtime
        self.NeedImage = 1
        while NotDone == 1:
            if (len(files) != 0):
                break
            else:
                files = filedialog.askopenfilenames() 

        self.FileChosen = files[0]  #store it for future refrence if needded*

        imageD = image.imread(self.FileChosen)

        self.imageData.append(imageD)

        #show OG image

        #pyplot.imshow(self.imageData[0]) <-- add back for comparison later?
        
        #remember to call pyplot.show() when done the other image processing
        
        return self
    def MainInstance(self):

        while self.run:

            screen.fill(self.background_colour)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = 0

            if (self.FilterMode == -1):
                self.SelectButton()
            else:   
                if (self.NeedImage == 0):
                    self.SelectImage()
                    #run image loader and make false once loaded image
                    #run filters
                    if (self.FilterMode == 0):
                        self.FilterBrightFrizz()
                    elif (self.FilterMode == 1):
                        #
                        pass
                    elif (self.FilterMode == 2):
                        #
                        pass
                    self.ShowBool = 1
                    self.tick += 1
                else:
                    screen.blit(self.D1, (0,0))
                    screen.blit(self.D2, (0,35))
                
                    

            pygame.display.update()
            
            if(self.tick!=0):
                self.tick+=1

            if(self.ShowBool and self.tick > 10):
                self.tick = 0
                pyplot.show()
                self.ShowBool = 0
#                pyplot.savefig('test.png', bbox_inches='tight',pad_inches = 0, dpi = 200)

        return self

PGI = pygameLogic()


PGI.MainInstance()
