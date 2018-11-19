import cv2
import numpy as np
from skimage import io
import os

# A class to handle image processing tasks to compute green cover percent
class Image_Processor:
    # initialize given latitude,longitude,width and height of the image and zoom value
    def __init__(self,lat,long,width=600,height=300,zoom=16):
        # get satellite image
        self.img = io.imread('https://maps.googleapis.com/maps/api/staticmap?center='+ str(lat)+','+str(long) + '&zoom='+str(zoom)+'&size=' + str(width) + 'x' + str(height) + '&maptype=satellite&key=AIzaSyDRjavHrEvei0wuHLRYUEbEtRH3YMGcKpQ')
        # convert to hsv
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        ## mask of green (36,0,0) ~ (70, 255,255)
        # apply mask to get binary image
        self.mask = cv2.inRange(self.hsv, (36,0,0), (86 ,255 ,255))
        # Fill all the white areas of the binary image with green
        imask = self.mask > 0
        green = np.zeros_like(self.img, np.uint8)
        green[imask] = self.img[imask]
        self.green = green
        self.green_percent = np.count_nonzero(self.mask)/self.mask.size * 100
        
    # store the image files for a given property id
    def store_images_for_pid(self,pid):
        if(not(os.path.isdir("static/images/properties/"+str(pid)))):
            os.mkdir("static/images/properties/"+str(pid))
        if(not(os.path.isdir("static/images/properties/"+str(pid)+"/greencover"))):
            os.mkdir("static/images/properties/"+str(pid)+"/greencover")
        cv2.imwrite("static/images/properties/"+str(pid)+"/greencover/input.png",self.img)
        cv2.imwrite("static/images/properties/"+str(pid)+"/greencover/hsv.png",self.hsv)
        cv2.imwrite("static/images/properties/"+str(pid)+"/greencover/mask.png",self.mask)
        cv2.imwrite("static/images/properties/"+str(pid)+"/greencover/green.png",self.green)