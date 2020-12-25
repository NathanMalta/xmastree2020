# DEBUGGING ONLY - SHOULD NOT BE TRANSFERED TO A RASPBERRY PI
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import board

class NeoPixel():
    '''A simulated neopixel library which displays an approximation of how the tree should look irl
       Created so code can be tested during development
    '''
    def __init__(self, digitalPin, numpixels, auto_write=True):
        #load pixel locations from file
        self.pixelLocations = self.getCoordsFromFile("coords.txt")
        self.pixelColors = [[0,0,0] for _ in range(numpixels)]

        #ensure neopixels are in correct configuration for hardware
        assert(digitalPin == board.D18)
        assert(numpixels == 500 == len(self.pixelLocations[0]))
        assert(len(self.pixelLocations[0]) == len(self.pixelLocations[1]) == len(self.pixelLocations[2]))
        assert(auto_write == False)

        #initialize matplotlib graphing stuff
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d', adjustable='box')
        self.ax.set_xlim(-460, 460)
        self.ax.set_ylim(-460, 460)
        self.ax.set_zlim(-460, 460)
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_zlabel('Z Axis')
        self.scatter = self.ax.scatter(self.pixelLocations[0], self.pixelLocations[1], self.pixelLocations[2])

    def getCoordsFromFile(self, filename):
        '''breaks the tree file down into a list of coordinates
        '''
        pixels = [[], [], []]
        with open(filename) as coordFile:
            for line in coordFile.readlines():
                line = line.replace('\n', '').replace(']', '').replace('[', '')
                coords = line.split(', ')
                pixels[0].append(int(coords[0]))
                pixels[1].append(int(coords[1]))
                pixels[2].append(int(coords[2]))

        return pixels

    def __setitem__(self, pixelNum, color):
        '''enables the syntax neopixel[pixelNum] = color
        '''
        #convert input (in GRB) into what matplotlib wants (in RGB)
        self.pixelColors[pixelNum] = [2 * color[1] / 255.0, 2 * color[0] / 255.0, 2 * color[2] / 255]

    def show(self):
        '''updates the tree animation when neopixel.show() is called
        '''

        self.scatter.remove()
        self.scatter = self.ax.scatter(self.pixelLocations[0], self.pixelLocations[1], self.pixelLocations[2], c=self.pixelColors)
        plt.draw()
        plt.pause(0.02)
        self.ax.cla()
        self.ax.set_xlim(-460, 460)
        self.ax.set_ylim(-460, 460)
        self.ax.set_zlim(-460, 460)
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_zlabel('Z Axis')

if __name__ == '__main__':
    pixels = NeoPixel(board.D18, 500, auto_write=False)