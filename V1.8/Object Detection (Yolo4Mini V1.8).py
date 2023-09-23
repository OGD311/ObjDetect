#Object detection
import cv2
import matplotlib.pyplot as plt

#cvlib
import cvlib as cv
from cvlib.object_detection import draw_bbox

#Multithreading
import threading

#Control Mouse and Keyboard
import keyboard as k
#import mouse as m
import pywinauto


#Screenshots
import numpy as np
from mss import mss
from PIL import Image

#FPS Measure
import time
import os
os.system("")

def drawcentrescreen(img):
    imgMax = img.shape
    maxH = imgMax[1]
    maxW = imgMax[0]
    scrCentre = [int(maxW/2),int(maxH/2)]
    for x in range(-2,2,1):
        for y in range(-2,2,1):
            img[scrCentre[0]+y][scrCentre[1]+x] = [0,0,255]

    return img, scrCentre


def drawcentreobject(img,bbox, draw=True):
    objCentres = []
    for item in bbox:
        startX = item[0]
        startY = item[1]
        endX = item[2]
        endY = item[3]

        objCentre = [(int((endY-startY)/2)+startY),(int((endX-startX)/2)+startX)]

        if draw == True:
            for x in range(-2,2,1):
                for y in range(-2,2,1):
                    img[objCentre[0]+y][objCentre[1]+x] = [255,0,0]

        objCentres.append(objCentre)
    return img, objCentres




def join(itm1, itm2):
    together = []
    for i in range(len(itm1)):
        together.append((itm1[i],itm2[i]))
    
    together = sorted(together, key=lambda together: together[1])

    for x in range(len(together)):
        itm1[x] = together[x][0]
        itm2[x] = together[x][1]

    return itm1, itm2


def lblNum(label):
    prev_label = label[0]
    lblVal = 0
    relabel = 0
    for q in range(0,len(label)):
        if label[q][-1].isdigit() == True:
            relabel = 1
            break
    
    if relabel == 0:
        for x in range(0,len(label)):
            if label[x] != prev_label:
                lblVal = 0
                
            label[x] = label[x]+str(lblVal)
            prev_label = label[x][:-1]
            lblVal += 1
    
    else:
        for i in range(0,len(label)):
            if label[i][-1].isdigit() == True:
                lblVal += 1
            
            if label[i][-1].isdigit() == False and label[i] != label[i+1]:
                label[i] = label[i] + str(lblVal)

            

    return label


def dirobj(bbox,last_bbox):
    directions = []
    if len(bbox) > len(last_bbox):
        q = len(bbox)
    else:
        q = len(last_bbox)
        
    for x in range(0,q):
        direction = ""
        lastX = last_bbox[x][1]
        lastY = last_bbox[x][0]

        curX = bbox[x][1]
        curY = bbox[x][0]

        if lastX > curX:
            direction += "left "
        elif lastX < curX:
            direction += "right "

        if lastY > curY:
            direction += "towards/downward "
        elif lastY < curY:
            direction += "away/upward "

        directions.append(direction)

    return directions


def speedobj(bbox, last_bbox):
    speeds = []

    if len(bbox) > len(last_bbox):
        q = len(bbox)
    else:
        q = len(last_bbox)
        
    for x in range(0,q):
        speed = 0
        lastX = last_bbox[x][1]
        lastY = last_bbox[x][0]

        curX = bbox[x][1]
        curY = bbox[x][0]


        distTrav = (((curX-lastX)**2) + ((curY-lastY)**2))*0.5

        speed = distTrav
        if speed == 0.0:
            speed = "constant (No change)"
        speeds.append(speed)
    
    return speeds

## OBJECT DETECTION ##
def objdetect(camera=False):
    last_bbox = ""
    last_label = ""

    while True:
        last_time = time.time()

        # Camera or Screencap
        if camera == True:
            success, img = imcap.read()
        else:
            img = np.array(sct.grab(mon))
            
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        #
  
        bbox, label, conf = cv.detect_common_objects(img, confidence=svar[0], model='yolov4-tiny')

        print((1 / (time.time()-last_time)))  
        # Join BBox and Label together and sort
        bbox, label = join(bbox,label)
        
        

        print((1 / (time.time()-last_time)))  
        # Numbered objects
        try:
            if bbox != last_bbox:
                label = lblNum(label)
            
            else:
                label = last_label
        except:
            pass
        #
        print((1 / (time.time()-last_time)))    
        output_image = draw_bbox(img, bbox, label, conf, write_conf=True)
        print((1 / (time.time()-last_time)))
        output_image, scrCentre = drawcentrescreen(output_image)
        print((1 / (time.time()-last_time)))
        output_image, objCentres = drawcentreobject(output_image,bbox,True)

        print((1 / (time.time()-last_time)))
        #Speed + Direction
        try:
            c, lastobjCentres = drawcentreobject(output_image,last_bbox, False)
            #Direction of object based on last position
            direction = dirobj(objCentres,lastobjCentres)

            #Speed of object based on last position in px/s
            speed = speedobj(objCentres,lastobjCentres)
        except:
            direction = []
            speed = []

        print((1 / (time.time()-last_time)))
        
        


        # Object Values
        fps = (1 / (time.time()-last_time))
        try:
            vals = []
            F = 1.3
            for i in range(len(label)):
                distance = (bbox[i][2] * F) / bbox[i][3]
                vals.append((label[i].title(), direction[i], speed[i]/distance, '{0:.2f} dist'.format(distance), '{0:.1f}%'.format(conf[i]*100)))
        except:
            vals = []
        #


        cv2.imshow('object_detect', output_image)



        # print FPS + other values
        fps = (1 / (time.time()-last_time))
        print('fps: {0:.2f}'.format(fps),*vals, end='\n',flush=True)
        print("\n \n \n")

        last_bbox = bbox
        last_label = label

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

























## MAIN ##
try:
    option = input("Camera/Screen (1/2): ")
except:
    option = "2"



#If camera is chosen
if option == "1":
    svar = [0.18,640,480]
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter camera width: ")), int(input("Enter camera height: "))]
    except:
        pass
        
    
    #print(svar)
    imcap = cv2.VideoCapture(0)

    imcap.set(3, svar[1]) # set width as 640
    imcap.set(4, svar[2])


    objdetect(True)
    # loop will be broken when 'q' is pressed on the keyboard


    cv2.destroyWindow('object_detect')
    raise ValueError("DONE")




#If screenshot is chosen
elif option == "2":
    svar = [0.185,160,160,640,400]
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter starting x: ")), int(input("Enter starting y: ")), int(input("Enter width: ")), int(input("Enter height: "))]
    except:
        pass
    
    print(svar)

    mon = {'top': svar[1], 'left': svar[2], 'width': svar[3], 'height': svar[4]}

    with mss() as sct: 
        objdetect()

        # loop will be broken when 'q' is pressed on the keyboard
        cv2.destroyWindow('object_detect')
        raise ValueError("DONE")
