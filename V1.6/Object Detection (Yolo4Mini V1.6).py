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


def objdetect(imcap,camera=False):
    if camera == True:
        success, img = imcap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    else:
        img = imcap
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    bbox, label, conf = cv.detect_common_objects(img, confidence=svar[0], model='yolov4-tiny')

    vals = []
    F = 1.3
    for i in range(len(label)):
        distance = (bbox[i][2] * F) / bbox[i][3]
        vals.append((label[i].title()+str(i),'{0:.2f}'.format(distance), '{0:.1f}%'.format(conf[i]*100)))

    ##Numbered objects
    try: 
        label.sort()
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

    cv2.imshow('object_detect', np.array(output_image))

    # print FPS
    print('fps: {0:.2f}'.format(1 / (time.time()-last_time)), *vals, '\033c', end='\r',flush=True)






##Main
option = input("Camera/Screen (1/2): ")
   
#If camera is chosen
if option == "1":
    svar = [0.18,640,480]
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter camera width: ")), int(input("Enter camera height: "))]
    except:
        pass
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
    svar = [0.18,160,160,800,400]
    try:
        svar = [float(input("Enter confidence (0.00-1.00): ")),int(input("Enter starting x: ")), int(input("Enter starting y: ")), int(input("Enter width: ")), int(input("Enter height: "))]
    except:
        pass

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
