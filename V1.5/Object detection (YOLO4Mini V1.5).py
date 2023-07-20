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

#Screenshot sizes
svar = [0.18,160,160,800,400,]
try:
    for i in range(len(svar)):
        inp = float(input(f"Num {i+1}: "))
        svar[i] = (inp)
except:
    pass

mon = {'top': svar[1], 'left': svar[2], 'width': svar[3], 'height': svar[4]}

#Object Detectionn
with mss() as sct:
    while True:
        last_time = time.time()
        img = sct.grab(mon)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

        bbox, label, conf = cv.detect_common_objects(np.array(img), confidence=svar[0], model='yolov4-tiny')

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
            
        output_image = draw_bbox(np.array(img), bbox, label, conf, write_conf=True)

        cv2.imshow('object_detect', np.array(output_image))

        # print FPS
        print('fps: {0:.2f}'.format(1 / (time.time()-last_time)), *vals, '\033c', end='\r',flush=True)


        # loop will be broken when 'q' is pressed on the keyboard
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('object_detect')
    raise ValueError("DONE")
