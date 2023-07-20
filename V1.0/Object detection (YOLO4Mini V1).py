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

vals = [160,160,400,400]
try:
    for i in range(0,4):
        inp = int(input(f"Num {i+1}: "))
        vals[i] = (inp)
except:
    pass

mon = {'top': vals[0], 'left': vals[1], 'width': vals[2], 'height': vals[3]}

with mss() as sct:
    while True:
        last_time = time.time()
        img = sct.grab(mon)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

        bbox, label, conf = cv.detect_common_objects(np.array(img), confidence=0.18, model='yolov4-tiny')

        vals = []
        for i in range(len(label)):
            distance = ((2 * 3.14 * 180) / (bbox[i][2] + bbox[i][3] * 360) * 1000 + 3)
            vals.append((label[i].title(),'{0:.2f}'.format(distance), '{0:.1f}%'.format(conf[i]*100)))


            
        output_image = draw_bbox(np.array(img), bbox, label, conf)

        

        

        cv2.imshow('object_detect', np.array(output_image))

        # print FPS
        print(vals,'fps: {0:.2f}'.format(1 / (time.time()-last_time)), end='\r',flush=True)


        # loop will be broken when 'q' is pressed on the keyboard
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('object_detect')
