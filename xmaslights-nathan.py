# Here are the libraries I am currently using:
import time
import board
import neopixel
import re
import math

# You are welcome to add any of these:
# import random
# import numpy
# import scipy
# import sys

def xmaslight():
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES (please don't break this bit)
    
    coordfilename = "Python/coords.txt" #TODO: change back to "coords.txt" if you want to debug on normal pc hardware!
	
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    # YOU CAN EDIT FROM HERE DOWN
    aHelper = AnimationHelper(pixels, coords)
    aHelper.animateBouncingBall()
    aHelper.makeParkerHead()
    aHelper.makePi()
    aHelper.makeHumblePi()
    aHelper.displayVid()
    print("done!")

class AnimationHelper:
    def __init__(self, pixels, coords):
        self.pixels = pixels
        self.coords = coords
    
    def animateBouncingBall(self):
        '''Runs a physics simulation of a playground ball bouncing and displays the result on the christmas tree
        '''

        print("animating ball...")
        #physics constants
        fGrav = -9.8 #in m/s^2; force of gravity
        mBall = 1 #in kg; mass of ball
        radBall = 0.75 #in meters; the radius of the ball
        kVal = 50 #Hooke's law k-value (modeling the ball as a spring)
        densityAir = 1.225 #in kg/m^3 #density of air at sea level
        dragCoeff = 0.05

        #simulation constants
        numTimesteps = 50 #how many updates the simulation should run for
        timestep = 0 #starting timestep number
        dt = 0.2 #how much time between each timestep

        #timestep specific properties of the ball
        height = 4 #in meters; height of the ball
        vel = 0 #in m/s; velocity of the ball

        #display constants
        metersToTree = 200 #how many "tree units" are in a simulation meter
        BALL_COLOR = [0, 50, 0]
        BACKGROUND_COLOR = [0, 0, 0]
        floorHeight = -200

        while timestep < numTimesteps:
            #update simulation

            #update bouncing force
            fSpring = 0
            if (height - radBall < 0):
                #ball is contacting the ground, spring force is occurring
                fSpring = abs(height - radBall) * kVal
            
            #update drag force
            #D = Cd * .5 * rho * V^2 * A as per https://www.grc.nasa.gov/www/k-12/airplane/dragsphere.html
            fDrag = dragCoeff * 0.5 * densityAir * (vel ** 2) * (math.pi * radBall ** 2) 
            fDrag = math.copysign(fDrag, -vel) #drag is in the opposite direction as velocity

            vel += (fGrav + fSpring + fDrag) / mBall * dt
            height += vel * dt

            #update tree
            for pixNum in range(len(self.coords)):
                xCenter = 0 
                yCenter = 0
                zCenter = height * metersToTree + floorHeight
                
                if ((self.coords[pixNum][0] - xCenter) ** 2 + (self.coords[pixNum][1] - yCenter) ** 2 + (self.coords[pixNum][2] - zCenter) ** 2) <= (radBall * metersToTree)**2:
                    self.pixels[pixNum] = BALL_COLOR
                else:
                    self.pixels[pixNum] = BACKGROUND_COLOR

            timestep += 1
            self.pixels.show()

    def makeParkerHead(self):
        print("displaying Matt Parker's head...")
        parkerHead = [[43, 54, 37],[40, 49, 33],[9, 10, 7],[9, 9, 8],[10, 11, 8],[9, 10, 7],[8, 8, 6], \
                    [7, 8, 6],[7, 8, 6],[75, 73, 74],[75, 73, 74],[9, 10, 7],[75, 73, 74],[7, 8, 6], \
                    [9, 9, 7],[9, 9, 7],[9, 10, 7],[9, 9, 7],[8, 9, 7],[41, 52, 34],[50, 62, 42], \
                    [32, 46, 26],[50, 70, 47],[44, 62, 36],[47, 66, 40],[38, 54, 32],[45, 62, 40],[50, 67, 43], \
                    [52, 66, 46],[41, 50, 35],[40, 49, 32],[43, 56, 34],[38, 49, 30],[38, 49, 30],[35, 41, 32], \
                    [38, 49, 30],[50, 65, 43],[38, 49, 30],[59, 59, 57],[43, 50, 36],[59, 59, 57],[48, 46, 47], \
                    [74, 72, 73],[75, 73, 74],[74, 73, 74],[75, 73, 74],[48, 45, 50],[18, 13, 21],[35, 41, 32], \
                    [46, 60, 37],[57, 70, 51],[39, 49, 34],[49, 61, 42],[37, 46, 32],[53, 67, 46],[29, 36, 23], \
                    [43, 55, 36],[50, 65, 45],[43, 55, 36],[39, 49, 34],[35, 44, 30],[38, 49, 30],[38, 48, 31], \
                    [45, 55, 36],[52, 66, 46],[38, 49, 30],[48, 61, 40],[40, 51, 32],[48, 46, 47],[67, 64, 65], \
                    [71, 68, 69],[48, 61, 40],[50, 65, 43],[40, 49, 32],[56, 67, 49],[34, 50, 29],[58, 73, 52], \
                    [47, 66, 44],[47, 66, 44],[36, 50, 32],[32, 50, 29],[50, 70, 47],[47, 66, 40],[47, 66, 40], \
                    [40, 61, 36],[53, 70, 49],[28, 43, 23],[57, 69, 50],[57, 68, 50],[50, 67, 43],[25, 32, 20], \
                    [29, 36, 25],[26, 32, 20],[22, 28, 17],[21, 27, 16],[32, 41, 26],[10, 11, 8],[7, 8, 5], \
                    [46, 57, 37],[46, 60, 38],[20, 24, 16],[45, 58, 34],[46, 57, 37],[31, 45, 23],[47, 59, 37], \
                    [51, 64, 40],[53, 67, 44],[47, 59, 37],[7, 8, 5],[3, 3, 3],[52, 65, 43],[41, 52, 34], \
                    [31, 45, 23],[52, 65, 43],[45, 58, 34],[7, 7, 4],[3, 4, 1],[8, 8, 6],[75, 73, 74], \
                    [3, 4, 1],[62, 60, 60],[4, 5, 3],[74, 73, 74],[7, 8, 6],[9, 9, 7],[9, 10, 7], \
                    [9, 9, 7],[9, 10, 7],[32, 41, 26],[40, 50, 32],[52, 65, 43],[46, 60, 38],[32, 46, 26], \
                    [52, 65, 43],[39, 49, 32],[51, 64, 41],[32, 46, 26],[44, 62, 36],[49, 61, 40],[52, 65, 43], \
                    [52, 65, 43],[49, 67, 44],[44, 67, 38],[38, 51, 34],[28, 43, 23],[28, 43, 23],[32, 53, 27], \
                    [34, 50, 29],[53, 70, 49],[35, 50, 32],[42, 57, 37],[49, 67, 44],[53, 77, 47],[46, 67, 40], \
                    [67, 87, 63],[67, 87, 63],[65, 88, 63],[61, 81, 57],[64, 85, 60],[28, 43, 23],[53, 70, 49], \
                    [53, 77, 47],[43, 60, 38],[43, 60, 35],[53, 73, 45],[47, 69, 40],[47, 64, 39],[43, 57, 35], \
                    [41, 52, 34],[52, 65, 43],[7, 8, 5],[0, 0, 0],[53, 66, 45],[53, 73, 45],[59, 78, 51], \
                    [61, 79, 52],[39, 58, 33],[49, 61, 40],[50, 63, 40],[57, 75, 46],[47, 61, 38],[46, 60, 38], \
                    [48, 60, 44],[48, 61, 39],[42, 58, 38],[39, 62, 33],[8, 7, 6],[23, 33, 20],[19, 20, 16], \
                    [1, 1, 0],[34, 33, 32],[4, 5, 2],[1, 2, 0],[0, 1, 0],[0, 0, 0],[1, 1, 0], \
                    [42, 58, 38],[48, 61, 39],[61, 80, 52],[61, 79, 52],[0, 0, 0],[1, 1, 0],[0, 1, 0], \
                    [5, 5, 3],[4, 5, 2],[7, 7, 5],[7, 7, 5],[7, 8, 5],[6, 6, 4],[3, 3, 3], \
                    [32, 39, 26],[50, 63, 42],[54, 67, 45],[53, 63, 48],[46, 61, 38],[57, 75, 46],[40, 55, 30], \
                    [36, 51, 25],[37, 50, 28],[35, 50, 28],[52, 69, 41],[52, 70, 41],[55, 72, 46],[58, 75, 47], \
                    [58, 75, 47],[54, 70, 43],[47, 58, 39],[57, 73, 46],[30, 40, 23],[35, 50, 28],[34, 46, 29], \
                    [42, 59, 32],[38, 55, 31],[57, 75, 46],[38, 55, 31],[40, 55, 30],[38, 55, 31],[36, 47, 28], \
                    [37, 50, 28],[35, 50, 28],[47, 62, 36],[17, 18, 14],[16, 16, 13],[8, 7, 6],[42, 58, 38], \
                    [1, 1, 0],[35, 44, 31],[2, 2, 1],[53, 67, 44],[20, 24, 16],[57, 79, 49],[45, 58, 34], \
                    [59, 78, 51],[63, 82, 56],[48, 72, 42],[61, 80, 52],[52, 72, 46],[52, 72, 46],[51, 73, 44], \
                    [61, 79, 52],[46, 67, 40],[52, 72, 46],[51, 73, 44],[51, 72, 45],[32, 38, 27],[65, 85, 61], \
                    [24, 35, 20],[38, 50, 31],[57, 76, 49],[57, 76, 48],[64, 81, 54],[63, 80, 54],[55, 72, 46], \
                    [33, 44, 26],[51, 67, 42],[43, 60, 36],[67, 85, 63],[40, 55, 34],[67, 85, 63],[40, 55, 34], \
                    [40, 55, 34],[59, 80, 50],[63, 85, 55],[49, 72, 42],[49, 72, 42],[41, 54, 32],[50, 68, 46], \
                    [50, 63, 41],[54, 64, 47],[32, 40, 26],[23, 29, 19],[32, 40, 26],[38, 49, 30],[45, 58, 36], \
                    [35, 45, 27],[35, 45, 27],[73, 70, 71],[75, 73, 74],[75, 73, 74],[21, 17, 26],[41, 50, 34], \
                    [48, 49, 46],[43, 55, 35],[50, 61, 41],[50, 63, 41],[50, 63, 41],[51, 65, 42],[42, 57, 36], \
                    [38, 52, 30],[58, 79, 51],[68, 86, 61],[63, 84, 56],[49, 72, 42],[52, 73, 44],[66, 79, 56], \
                    [63, 84, 56],[45, 63, 35],[36, 54, 29],[38, 51, 32],[41, 55, 32],[39, 52, 32],[41, 55, 32], \
                    [61, 76, 52],[60, 78, 50],[50, 63, 41],[58, 74, 49],[57, 74, 50],[35, 45, 30],[16, 16, 14], \
                    [11, 11, 9],[15, 16, 13],[62, 60, 60],[67, 64, 66],[67, 64, 66],[50, 49, 49],[49, 48, 48], \
                    [25, 25, 24],[11, 11, 9],[14, 15, 12],[45, 58, 36],[45, 58, 36],[37, 56, 28],[60, 82, 54], \
                    [45, 63, 37],[42, 58, 33],[52, 66, 42],[16, 17, 14],[48, 63, 40],[61, 72, 52],[57, 69, 49], \
                    [53, 68, 43],[60, 74, 50],[20, 21, 17],[20, 21, 17],[44, 56, 36],[57, 74, 50],[67, 84, 62], \
                    [20, 21, 17],[61, 72, 52],[18, 20, 16],[25, 25, 24],[27, 27, 25],[49, 48, 48],[72, 70, 70], \
                    [74, 73, 74],[72, 69, 70],[67, 64, 65],[17, 18, 15],[46, 57, 38],[25, 25, 24],[14, 15, 12], \
                    [41, 54, 32],[38, 52, 30],[51, 63, 43],[48, 46, 47],[54, 66, 45],[72, 69, 70],[74, 72, 73], \
                    [74, 71, 72],[74, 72, 73],[66, 62, 64],[42, 41, 40],[72, 70, 71],[17, 18, 15],[15, 16, 13], \
                    [18, 19, 16],[18, 20, 15],[56, 68, 47],[61, 72, 52],[60, 74, 50],[58, 74, 50],[62, 80, 53], \
                    [62, 80, 53],[64, 78, 54],[64, 78, 54],[57, 74, 47],[52, 65, 43],[61, 76, 52],[61, 76, 52], \
                    [66, 82, 56],[60, 74, 51],[27, 33, 23],[27, 31, 24],[35, 47, 31],[40, 55, 35],[65, 83, 58], \
                    [43, 60, 36],[56, 76, 48],[30, 40, 23],[50, 62, 40],[52, 69, 41],[52, 70, 41],[54, 70, 43], \
                    [54, 73, 44],[61, 78, 51],[64, 81, 54],[51, 69, 43],[60, 74, 51],[61, 76, 52],[61, 76, 52], \
                    [57, 74, 47],[57, 74, 47],[40, 48, 32],[57, 73, 46],[62, 77, 52],[68, 81, 58],[68, 81, 58], \
                    [63, 80, 54],[60, 78, 52],[62, 80, 54],[65, 83, 58],[63, 81, 55],[66, 83, 58],[63, 81, 55], \
                    [62, 80, 53],[63, 80, 54],[63, 80, 54],[62, 80, 53],[63, 81, 55],[66, 83, 57],[40, 54, 32], \
                    [38, 49, 30],[66, 83, 58],[63, 78, 52],[66, 83, 58],[61, 78, 49],[65, 81, 56],[60, 78, 52], \
                    [65, 81, 55],[74, 87, 68],[70, 85, 64],[71, 80, 65],[67, 75, 61],[60, 68, 53],[72, 86, 66], \
                    [72, 85, 66],[69, 86, 64],[67, 83, 60],[67, 83, 60],[71, 84, 63],[80, 89, 74],[71, 84, 63], \
                    [62, 70, 54],[75, 87, 69],[79, 89, 73],[78, 87, 72],[85, 92, 79],[49, 56, 43],[53, 63, 45], \
                    [36, 39, 32],[20, 19, 18],[79, 85, 74],[79, 85, 74],[60, 69, 54],[31, 30, 29],[24, 23, 22], \
                    [19, 18, 16],[19, 18, 16],[28, 36, 22],[26, 32, 20],[21, 21, 19],[29, 28, 27],[37, 43, 32], \
                    [69, 76, 65],[69, 76, 65],[70, 81, 65],[72, 86, 67],[71, 86, 66],[69, 81, 64],[66, 73, 61], \
                    [72, 86, 67],[68, 78, 63],[80, 90, 75],[76, 83, 70],[78, 88, 74],[79, 89, 73],[75, 87, 69], \
                    [65, 81, 55],[65, 82, 57],[63, 81, 55]]
        
        self.displayImg(parkerHead)
        time.sleep(10)

    def makePi(self):
        print("displaying pi...")
        pi = [[0, 0, 0],[0, 0, 0],[0, 12, 74],[0, 12, 74],[0, 12, 72],[0, 12, 73],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 1], \
            [0, 0, 0],[0, 10, 61],[0, 12, 75],[0, 12, 74],[0, 12, 75],[0, 13, 75],[0, 11, 65], \
            [0, 2, 11],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 10, 57],[0, 12, 75],[0, 12, 73],[0, 12, 74],[0, 12, 74],[0, 12, 75], \
            [0, 12, 74],[0, 12, 74],[0, 12, 74],[0, 6, 37],[0, 0, 1],[0, 6, 37],[0, 0, 1], \
            [0, 10, 64],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 2, 13],[0, 5, 28],[0, 12, 75], \
            [0, 13, 75],[0, 0, 2],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 12, 74],[0, 4, 22], \
            [0, 12, 74],[0, 0, 0],[0, 12, 74],[0, 12, 75],[0, 13, 75],[0, 0, 1],[0, 5, 28], \
            [0, 13, 75],[0, 12, 75],[0, 12, 74],[0, 12, 75],[0, 1, 8],[0, 4, 25],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 13, 75],[0, 12, 75],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 13, 75],[0, 12, 72],[0, 8, 49], \
            [0, 13, 75],[0, 12, 74],[0, 0, 0],[0, 12, 75],[0, 13, 75],[0, 1, 6],[0, 11, 67], \
            [0, 9, 52],[0, 6, 37],[0, 11, 67],[0, 1, 8],[0, 0, 0],[0, 12, 75],[0, 13, 75], \
            [0, 1, 6],[0, 12, 75],[0, 12, 75],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 3],[0, 12, 74],[0, 13, 75],[0, 8, 49],[0, 12, 75],[0, 12, 74],[0, 2, 11], \
            [0, 12, 75],[0, 13, 75],[0, 12, 75],[0, 2, 11],[0, 0, 0],[0, 10, 58],[0, 12, 75], \
            [0, 12, 75],[0, 0, 0],[0, 6, 35],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 0], \
            [0, 4, 25],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 0], \
            [0, 0, 1],[0, 0, 0],[0, 12, 75],[0, 13, 75],[0, 13, 75],[0, 13, 75],[0, 12, 70], \
            [0, 13, 75],[0, 12, 75],[0, 8, 49],[0, 0, 0],[0, 4, 25],[0, 13, 75],[0, 12, 75], \
            [0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 11, 64],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 1, 8],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 2, 16],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 9, 56], \
            [0, 0, 0],[0, 0, 0],[0, 8, 47],[0, 0, 0],[0, 0, 0],[0, 12, 73],[0, 6, 35], \
            [0, 6, 35],[0, 0, 0],[0, 0, 0],[0, 0, 2],[0, 7, 41],[0, 8, 47],[0, 9, 53], \
            [0, 13, 75],[0, 13, 75],[0, 0, 0],[0, 13, 75],[0, 9, 56],[0, 13, 75],[0, 0, 0], \
            [0, 0, 0],[0, 8, 47],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 6, 37],[0, 0, 0],[0, 13, 75],[0, 12, 75], \
            [0, 12, 75],[0, 12, 72],[0, 7, 41],[0, 11, 64],[0, 0, 0],[0, 0, 0],[0, 8, 46], \
            [0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 8, 46],[0, 0, 0],[0, 13, 75],[0, 0, 0], \
            [0, 13, 75],[0, 13, 75],[0, 1, 8],[0, 0, 0],[0, 2, 13],[0, 12, 75],[0, 12, 73], \
            [0, 13, 75],[0, 12, 69],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 12, 75],[0, 12, 75],[0, 13, 75],[0, 13, 75],[0, 3, 20],[0, 5, 25], \
            [0, 13, 75],[0, 12, 75],[0, 13, 75],[0, 0, 0],[0, 13, 75],[0, 12, 74],[0, 12, 74], \
            [0, 12, 74],[0, 12, 74],[0, 12, 72],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 12, 71], \
            [0, 0, 0],[0, 10, 59],[0, 6, 38],[0, 13, 75],[0, 13, 75],[0, 12, 75],[0, 13, 75], \
            [0, 3, 16],[0, 12, 75],[0, 13, 75],[0, 13, 75],[0, 13, 75],[0, 12, 75],[0, 0, 0], \
            [0, 13, 75],[0, 12, 74],[0, 2, 12],[0, 1, 9],[0, 13, 75],[0, 0, 0],[0, 13, 75], \
            [0, 0, 0],[0, 6, 35],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 11, 65],[0, 11, 65],[0, 5, 34],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 3, 17],[0, 3, 17],[0, 13, 75],[0, 13, 75], \
            [0, 12, 75],[0, 12, 75],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 12, 74], \
            [0, 0, 0],[0, 12, 72],[0, 5, 28],[0, 0, 0],[0, 0, 1],[0, 0, 0],[0, 0, 0], \
            [0, 3, 20],[0, 3, 16],[0, 0, 0],[0, 0, 1],[0, 3, 20],[0, 12, 72],[0, 10, 64], \
            [0, 13, 75],[0, 10, 64],[0, 6, 36],[0, 0, 0],[0, 2, 14],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 3, 20],[0, 5, 29], \
            [0, 5, 29],[0, 0, 0],[0, 0, 0],[0, 8, 50],[0, 13, 75],[0, 9, 54],[0, 9, 54], \
            [0, 8, 50],[0, 0, 0],[0, 11, 67],[0, 0, 4],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 1],[0, 0, 0],[0, 7, 41],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 5, 29],[0, 13, 75],[0, 2, 13],[0, 0, 0],[0, 0, 0],[0, 9, 54],[0, 9, 54], \
            [0, 10, 59],[0, 10, 59],[0, 0, 2],[0, 10, 64],[0, 12, 72],[0, 12, 75],[0, 12, 75], \
            [0, 3, 18],[0, 0, 0],[0, 0, 0],[0, 3, 18],[0, 0, 0],[0, 12, 75],[0, 0, 0], \
            [0, 2, 15],[0, 13, 75],[0, 13, 75],[0, 2, 15],[0, 0, 1],[0, 0, 0],[0, 0, 0], \
            [0, 10, 58],[0, 0, 0],[0, 13, 75],[0, 0, 0],[0, 13, 75],[0, 3, 19],[0, 0, 0], \
            [0, 13, 75],[0, 12, 75],[0, 12, 75],[0, 12, 73],[0, 13, 75],[0, 4, 20],[0, 12, 75], \
            [0, 12, 75],[0, 12, 74],[0, 13, 75],[0, 13, 75],[0, 12, 74],[0, 13, 75],[0, 12, 74], \
            [0, 12, 75],[0, 12, 75],[0, 12, 73],[0, 13, 75],[0, 7, 40],[0, 0, 0],[0, 0, 1], \
            [0, 0, 0],[0, 0, 0],[0, 0, 1],[0, 0, 1],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0], \
            [0, 0, 1],[0, 0, 1],[0, 7, 40],[0, 12, 73],[0, 12, 73],[0, 7, 40],[0, 0, 0], \
            [0, 12, 73],[0, 7, 40],[0, 12, 73],[0, 0, 0],[0, 13, 75],[0, 12, 73],[0, 12, 75], \
            [0, 13, 75],[0, 13, 75],[0, 0, 0]]
        
        self.displayImg(pi)
        time.sleep(10)
        

    def makeHumblePi(self):
        print("displaying humble pi...")
        humblePi = [[72, 74, 67],[59, 60, 56],[52, 53, 49],[67, 68, 62],[68, 70, 64],[65, 67, 61],[72, 75, 68], \
                    [72, 75, 68],[72, 75, 68],[72, 74, 67],[72, 74, 67],[72, 74, 67],[72, 74, 67],[72, 75, 68], \
                    [72, 75, 68],[74, 75, 69],[50, 52, 47],[22, 23, 22],[57, 58, 54],[45, 46, 42],[46, 50, 43], \
                    [26, 48, 25],[71, 73, 66],[72, 74, 67],[75, 75, 71],[72, 74, 67],[75, 75, 70],[47, 47, 43], \
                    [69, 70, 65],[66, 67, 62],[61, 62, 57],[35, 35, 33],[41, 42, 39],[65, 66, 61],[74, 75, 69], \
                    [65, 66, 61],[65, 67, 60],[41, 42, 39],[51, 52, 48],[34, 35, 32],[51, 52, 48],[75, 75, 70], \
                    [72, 74, 67],[72, 74, 67],[72, 74, 67],[72, 74, 67],[73, 75, 68],[72, 74, 67],[74, 75, 69], \
                    [74, 75, 69],[68, 69, 63],[45, 46, 43],[75, 75, 72],[73, 75, 68],[58, 59, 55],[52, 52, 49], \
                    [73, 74, 70],[73, 74, 70],[73, 74, 70],[45, 46, 43],[36, 36, 34],[41, 42, 39],[43, 44, 41], \
                    [43, 44, 41],[69, 70, 65],[65, 66, 61],[67, 68, 63],[60, 62, 57],[75, 75, 70],[72, 74, 67], \
                    [75, 75, 70],[67, 68, 63],[65, 67, 60],[61, 62, 57],[26, 27, 25],[38, 39, 36],[48, 49, 46], \
                    [48, 48, 45],[48, 48, 45],[75, 75, 74],[66, 71, 62],[71, 73, 66],[75, 75, 71],[75, 75, 71], \
                    [73, 74, 68],[61, 63, 57],[65, 68, 62],[47, 48, 44],[35, 36, 33],[47, 47, 43],[69, 71, 65], \
                    [69, 70, 65],[72, 74, 67],[73, 75, 68],[70, 72, 65],[69, 70, 65],[68, 70, 64],[67, 69, 63], \
                    [41, 42, 39],[60, 60, 57],[72, 75, 67],[58, 59, 54],[41, 42, 39],[37, 41, 35],[66, 67, 62], \
                    [74, 75, 69],[72, 74, 67],[66, 67, 62],[74, 75, 69],[73, 75, 68],[50, 52, 47],[45, 46, 42], \
                    [37, 41, 35],[50, 52, 47],[58, 59, 54],[72, 74, 67],[72, 75, 68],[72, 75, 68],[72, 74, 67], \
                    [72, 75, 68],[72, 74, 67],[72, 75, 68],[72, 74, 67],[72, 75, 68],[72, 75, 68],[72, 74, 67], \
                    [72, 75, 68],[52, 53, 49],[69, 70, 65],[45, 46, 42],[50, 52, 47],[60, 60, 57],[26, 48, 25], \
                    [50, 52, 47],[50, 52, 47],[49, 49, 45],[26, 48, 25],[72, 74, 67],[54, 54, 50],[50, 52, 47], \
                    [50, 52, 47],[37, 60, 35],[71, 74, 66],[74, 74, 70],[65, 68, 62],[65, 68, 62],[31, 54, 30], \
                    [38, 39, 36],[61, 63, 57],[75, 75, 74],[75, 75, 73],[37, 60, 35],[51, 65, 48],[40, 41, 37], \
                    [61, 62, 57],[61, 62, 57],[27, 28, 25],[35, 35, 32],[68, 71, 64],[65, 68, 62],[61, 63, 57], \
                    [51, 65, 48],[27, 60, 25],[75, 75, 75],[72, 75, 67],[72, 74, 66],[72, 74, 67],[34, 39, 32], \
                    [45, 46, 42],[50, 52, 47],[67, 69, 63],[72, 75, 68],[72, 75, 68],[72, 75, 67],[72, 75, 67], \
                    [72, 75, 68],[72, 75, 68],[68, 72, 63],[73, 75, 69],[72, 75, 67],[72, 75, 68],[72, 75, 68], \
                    [72, 75, 68],[72, 75, 67],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 74, 67], \
                    [72, 75, 68],[72, 74, 67],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68], \
                    [72, 75, 68],[72, 75, 67],[72, 75, 67],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68], \
                    [72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 74, 67],[74, 75, 69],[74, 75, 69],[73, 75, 68], \
                    [72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 67],[74, 74, 69], \
                    [68, 72, 64],[42, 68, 37],[44, 68, 40],[72, 75, 67],[72, 75, 67],[50, 68, 45],[73, 75, 67], \
                    [73, 75, 67],[66, 72, 61],[61, 72, 56],[75, 75, 71],[72, 74, 67],[44, 68, 40],[66, 71, 61], \
                    [72, 75, 67],[73, 74, 68],[72, 75, 67],[73, 74, 68],[74, 74, 69],[73, 74, 68],[37, 68, 32], \
                    [42, 68, 37],[44, 68, 40],[72, 75, 67],[72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 75, 68], \
                    [72, 75, 68],[72, 75, 68],[72, 75, 68],[72, 74, 67],[72, 75, 67],[72, 75, 67],[58, 59, 54], \
                    [72, 75, 67],[72, 75, 67],[72, 74, 67],[72, 75, 67],[73, 75, 68],[73, 75, 68],[74, 75, 70], \
                    [72, 75, 68],[40, 41, 37],[73, 75, 68],[74, 75, 70],[60, 62, 56],[70, 73, 66],[70, 73, 65], \
                    [50, 69, 45],[71, 74, 65],[34, 67, 29],[66, 72, 62],[75, 75, 73],[31, 66, 25],[50, 68, 45], \
                    [68, 73, 62],[62, 71, 57],[36, 67, 30],[72, 74, 68],[70, 74, 65],[72, 74, 68],[70, 74, 65], \
                    [70, 74, 65],[46, 47, 43],[75, 75, 71],[40, 61, 38],[40, 61, 38],[66, 74, 62],[74, 72, 69], \
                    [29, 52, 27],[58, 59, 54],[63, 64, 59],[62, 64, 59],[63, 64, 59],[65, 66, 61],[65, 67, 61], \
                    [62, 63, 58],[62, 63, 58],[59, 60, 56],[73, 74, 68],[73, 74, 68],[72, 74, 67],[25, 25, 23], \
                    [36, 37, 34],[50, 51, 46],[45, 47, 42],[29, 52, 27],[29, 52, 27],[22, 51, 21],[33, 34, 32], \
                    [54, 61, 51],[64, 64, 61],[72, 74, 68],[71, 74, 67],[40, 61, 38],[27, 55, 25],[72, 75, 67], \
                    [71, 74, 67],[22, 24, 20],[57, 60, 53],[40, 69, 35],[61, 71, 56],[41, 68, 36],[61, 71, 56], \
                    [65, 72, 60],[45, 69, 40],[75, 75, 72],[61, 62, 58],[72, 75, 68],[72, 75, 68],[72, 74, 67], \
                    [72, 74, 67],[72, 75, 68],[72, 74, 67],[72, 74, 67],[72, 74, 67],[72, 74, 67],[72, 74, 67], \
                    [72, 74, 67],[72, 74, 67],[74, 75, 71],[32, 38, 31],[32, 38, 31],[46, 61, 44],[75, 75, 72], \
                    [14, 55, 13],[23, 58, 22],[48, 49, 45],[73, 75, 68],[24, 23, 23],[72, 74, 67],[52, 52, 48], \
                    [75, 75, 71],[73, 74, 69],[72, 75, 68],[72, 75, 68],[73, 74, 69],[72, 75, 68],[74, 74, 69], \
                    [72, 75, 68],[72, 74, 67],[72, 75, 68],[72, 74, 67],[75, 75, 70],[72, 74, 67],[72, 74, 67], \
                    [72, 74, 67],[71, 73, 67],[72, 74, 67],[75, 75, 71],[35, 36, 33],[72, 74, 67],[74, 75, 71], \
                    [66, 74, 62],[54, 61, 51],[35, 36, 34],[75, 75, 70],[64, 68, 60],[71, 73, 67],[72, 74, 67], \
                    [74, 75, 69],[72, 74, 67],[74, 74, 70],[72, 74, 67],[72, 74, 67],[75, 75, 71],[72, 75, 68], \
                    [72, 74, 67],[72, 75, 68],[72, 75, 68],[72, 74, 67],[73, 74, 69],[71, 73, 67],[50, 52, 47], \
                    [50, 52, 47],[43, 68, 37],[43, 68, 37],[70, 73, 65],[48, 70, 44],[75, 75, 71],[75, 75, 71], \
                    [64, 72, 60],[74, 73, 70],[72, 73, 67],[64, 72, 59],[27, 67, 22],[31, 67, 26],[57, 71, 52], \
                    [36, 67, 30],[67, 72, 63],[72, 74, 67],[75, 75, 70],[72, 75, 67],[72, 75, 67],[66, 72, 61], \
                    [53, 69, 49],[33, 67, 28],[75, 75, 73],[56, 70, 50],[74, 73, 70],[75, 75, 71],[75, 75, 71], \
                    [75, 75, 71],[75, 75, 71],[63, 71, 58],[54, 70, 49],[57, 71, 51],[75, 74, 73],[75, 74, 73], \
                    [40, 68, 35],[24, 66, 19],[67, 73, 62],[66, 72, 62],[50, 70, 45],[75, 74, 73],[50, 70, 45], \
                    [35, 66, 30],[56, 71, 50],[56, 71, 50],[35, 66, 30],[72, 74, 68],[70, 73, 65],[33, 67, 28], \
                    [58, 70, 53],[61, 71, 57],[75, 75, 72],[61, 71, 57],[61, 71, 56],[37, 67, 31],[24, 66, 19], \
                    [72, 73, 67],[30, 67, 25],[52, 70, 48],[44, 68, 38],[71, 72, 66],[74, 75, 70],[35, 68, 30], \
                    [35, 67, 28],[59, 71, 55],[75, 74, 71],[75, 74, 71],[53, 70, 48],[72, 73, 67],[53, 70, 48], \
                    [38, 68, 34],[28, 66, 23],[55, 70, 50],[75, 75, 71],[75, 75, 71],[73, 74, 67],[15, 15, 15], \
                    [31, 32, 30],[66, 68, 62],[32, 32, 30],[32, 32, 30],[75, 75, 72],[68, 69, 64],[74, 75, 69], \
                    [73, 75, 68],[73, 75, 68],[72, 74, 67],[72, 74, 67],[72, 74, 68],[65, 67, 62],[66, 68, 62], \
                    [31, 31, 29],[31, 31, 29],[74, 75, 69],[62, 71, 58],[62, 72, 57],[75, 75, 70],[57, 58, 54], \
                    [62, 71, 58],[75, 75, 71],[42, 70, 38],[57, 59, 54],[71, 72, 66],[55, 70, 50],[28, 66, 23], \
                    [72, 73, 67],[71, 72, 66],[35, 68, 30]]

        self.displayImg(humblePi)
        time.sleep(10)

    def displayVid(self):
        import vid #don't import until down here in case we can't find the vid file

        print("playing video...")
        for frame in vid.vid:
            self.displayImg(frame)


    def displayImg(self, colorList):
        for i in range(len(self.coords)):
            self.pixels[i] = colorList[i]

        self.pixels.show()


# yes, I just put this at the bottom so it auto runs
xmaslight()
