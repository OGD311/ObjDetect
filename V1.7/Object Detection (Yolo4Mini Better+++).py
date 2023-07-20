#Object detection
import cv2
import matplotlib.pyplot as plt

#cvlib
import cvlib as cv
from cvlib.object_detection import draw_bbox

#Screenshots
import numpy as np
from mss import mss
from PIL import Image

#FPS Measure
import time

def drawcentrescreen(img):
    imgMax = img.shape
    maxH = imgMax[1]
    maxW = imgMax[0]
    scrCentre = [int(maxW/2),int(maxH/2)]
    for x in range(-2,2,1):
        for y in range(-2,2,1):
            img[scrCentre[0]+y][scrCentre[1]+x] = [0,0,255]

    return img, scrCentre

def drawcentreobject(img,bbox):
    objCentres = []
    for item in bbox:
        startX = item[0]
        startY = item[1]
        endX = item[2]
        endY = item[3]

        objCentre = [(int((endY-startY)/2)+startY),(int((endX-startX)/2)+startX)]
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

def objdetect(imcap,camera=False):
    ##Camera or Screencap
    if camera == True:
        success, img = imcap.read()
    else:
        img = imcap
        
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    ##

    
    bbox, label, conf = cv.detect_common_objects(img, confidence=svar[0], model='yolov4-tiny')

    ##Object Values
    vals = []
    F = 1.3
    for i in range(len(label)):
        distance = (bbox[i][2] * F) / bbox[i][3]
        vals.append((label[i].title()+str(i),'{0:.2f}'.format(distance), '{0:.1f}%'.format(conf[i]*100)))
    ##

    ##Join BBox and Label together before sorting
    bbox, label = join(bbox,label)
    

    ##Numbered objects
    try: 
        prev_label = label[0]
        o = 0
        for x in range(0,len(label)):
            if label[x] != prev_label:
                o = 0
                
            label[x] = label[x]+str(o)
            prev_label = label[x][:-1]
            o += 1

    except:
        pass
    ##
        
    output_image = draw_bbox(img, bbox, label, conf, write_conf=True)
    
    output_image, scrCentre = drawcentrescreen(output_image)
    output_image, objCentres = drawcentreobject(output_image,bbox)

    cv2.imshow('object_detect', np.array(output_image))

    # print FPS
    print('fps: {0:.2f}'.format(1 / (time.time()-last_time)), *vals, '\033c', end='\r',flush=True)


def objmove(objcentre,scrcentre):
    print()



##Main
try:
    option = input("Camera/Screen (1/2): ")
except:
    option = "2"


#If camera is chosen
if option == "1":
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter camera width: ")), int(input("Enter camera height: "))]
    except:
        svar = [0.18,640,480]
    imcap = cv2.VideoCapture(0)

    imcap.set(3, svar[1]) # set width as 640
    imcap.set(4, svar[2])


    while True:
        last_time = time.time()
        objdetect(imcap,True)
            # loop will be broken when 'q' is pressed on the keyboard
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyWindow('object_detect')
    raise ValueError("DONE")




#If screenshot is chosen
elif option == "2":
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter starting x: ")), int(input("Enter starting y: ")), int(input("Enter width: ")), int(input("Enter height: "))]
    except:
        svar = [0.185,160,160,1280,800]

    mon = {'top': svar[1], 'left': svar[2], 'width': svar[3], 'height': svar[4]}

    with mss() as sct:
        while True:
            last_time = time.time()
            img = sct.grab(mon)
            objdetect(np.array(img))
            # loop will be broken when 'q' is pressed on the keyboard
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cv2.destroyWindow('object_detect')
        raise ValueError("DONE")
