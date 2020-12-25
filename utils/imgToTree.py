from PIL import Image
import sys

class ImgToTree:
    '''A class which takes in a png file and converts it into an array of colors for the tree
    '''
    def __init__(self, imgFile, treeFile):
        self.im = Image.open(imgFile).convert('RGB')
        self.coords = self.getCoordsFromFile(treeFile)

    def imgToColors(self):
        maxBrightness = 75 #defines maximum brightness of a subpixel

        #resize image so it can fit on the tree
        qualityFactor = 0.05
        width = int((abs(min(self.coords[0])) + abs(max(self.coords[0]))) * qualityFactor)
        height = int((abs(min(self.coords[2])) + abs(max(self.coords[2]))) * qualityFactor) 
        self.im = self.im.resize((width,height), Image.ANTIALIAS)
        self.im.save("test.png", "PNG")

        colors = []
        xMin = min(self.coords[0])
        yMin = min(self.coords[2])
        for i in range(len(self.coords[0])):
            #convert to point on the image
            xPos = int((self.coords[0][i] - xMin) * qualityFactor) - 1
            yPos = height - int((self.coords[2][i] - yMin) * qualityFactor) - 1
            r, g, b = self.im.getpixel((xPos, yPos))
            # self.im.putpixel((xPos, yPos), (0, 0, 0))
            r = int((r / 255.0) * maxBrightness)
            g = int((g / 255.0) * maxBrightness)
            b = int((b / 255.0) * maxBrightness)

            colors.append([g, r, b])
        self.im.save("output.png", "PNG")
        return colors


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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python imgToTree.py [path to img] [path to coords.txt]")
    else:
        imgToTree = ImgToTree(sys.argv[1], sys.argv[2])
        colorArr = imgToTree.imgToColors()
        colorArrStr = "["
        for i in range(len(colorArr)):
            if i != 0 and i % 7 == 0:
                colorArrStr += " \\\n"
            colorArrStr += str(colorArr[i])
            if i != len(colorArr) - 1:
                colorArrStr += ","
        colorArrStr += "]"
        print()
        print()
        print(colorArrStr)
        