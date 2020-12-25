from PIL import Image
import cv2
import os
import sys

class VidToTree:
    '''A class which takes in a mp4 file and converts it into an array of frames (2D array of pixels or 3D array of subpixels)
       for display on the tree 
    '''
    def __init__(self, vidFile, treeFile):
        self.vidcap = cv2.VideoCapture(vidFile)
        self.coords = self.getCoordsFromFile(treeFile)
        

    def vidToColors(self):
        maxBrightness = 75 #defines maximum brightness of a subpixel

        #determine image sizes so it can fit on the tree
        qualityFactor = 0.05
        width = int((abs(min(self.coords[0])) + abs(max(self.coords[0]))) * qualityFactor)
        height = int((abs(min(self.coords[2])) + abs(max(self.coords[2]))) * qualityFactor) 

        xMin = min(self.coords[0])
        yMin = min(self.coords[2])

        videoArr = []

        #read video and convert to color array
        success = True
        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 24, (width,height))
        while success:
            frame = []
            #read frame of video
            success, img_cv = self.vidcap.read()

            #resize to christmas tree
            if img_cv is None or len(img_cv) == 0:
                continue #ignore empty frames

            img_cv = cv2.resize(img_cv, (width, height))
            out.write(img_cv)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img_cv)

            for i in range(len(self.coords[0])):
                #convert to point on the image
                xPos = int((self.coords[0][i] - xMin) * qualityFactor) - 1
                yPos = height - int((self.coords[2][i] - yMin) * qualityFactor) - 1
                r, g, b = im_pil.getpixel((xPos, yPos))
                # self.im.putpixel((xPos, yPos), (0, 0, 0))
                r = int((r / 255.0) * maxBrightness)
                g = int((g / 255.0) * maxBrightness)
                b = int((b / 255.0) * maxBrightness)

                frame.append([g, r, b])
            videoArr.append(frame)
        return videoArr


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
        print("usage: python vidToTree.py [path to vid] [path to coords.txt]")
    else:
        vidToTree = VidToTree(sys.argv[1], sys.argv[2])
        vidArr = vidToTree.vidToColors()

        with open("vid.py", "w") as f:
            f.write(f"vid = {str(vidArr)}")
        