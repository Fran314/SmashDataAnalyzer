import time
import numpy
import pytesseract
from cv2 import cv2
import re
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# pylint: disable=import-error
import functions as fun


# BACKGROUND_ICONS_BGRS = [[32, 27, 172],
#                         [181, 90, 21],
#                         [0, 125, 166],
#                         [22, 131, 22]]

RIGHT_EDGE = [423, 842, 1261]
LEFT_EDGE = [19, 438, 857]

screenshots = os.listdir(r'C:\Users\franc\Desktop\aptest')
template_source = cv2.imread(r'C:\Users\franc\Documents\VSCode\SmashDataCollector\res\temp\template.png')
templates = [template_source[:, 0:8].copy(), template_source[:, 8:16].copy(), template_source[:, 16:24].copy()]
height = templates[0].shape[0]
span_range = int(height * 3.0 / 4.0)

for screenshot_file in screenshots:
    screenshot_image = cv2.imread(os.path.join(r'C:\Users\franc\Desktop\aptest', screenshot_file))
    for i in range(3):
        subimage = screenshot_image[172 : 443, RIGHT_EDGE[i] - 19 : RIGHT_EDGE[i] - 11].copy()
        distances = cv2.matchTemplate(subimage, templates[i], cv2.TM_CCOEFF_NORMED)
        found = False
        for j in range(distances.shape[0]):
            upper_span = min(j, span_range)
            lower_span = min(distances.shape[0] - j - 1, span_range)
            region = distances[j - upper_span : j + lower_span]
            if(numpy.argmax(region) == upper_span and
                numpy.sum(fun.polarizeImage(screenshot_image[174 + j : 172 + j + height - 2, RIGHT_EDGE[i] - 19 - 20 : RIGHT_EDGE[i] - 19], 100)) == 0 and
                numpy.sum(fun.polarizeImage(screenshot_image[174 + j + 74 : 172 + j + height - 2 + 74, RIGHT_EDGE[i] - 19 - 20 : RIGHT_EDGE[i] - 19], 100)) > 0):
                fun.showImage(screenshot_image[172 + j : 172 + j + height, LEFT_EDGE[i] : RIGHT_EDGE[i]])
                found = True
                break
        if(found == False):
            print('Errr... couldn\'t find it...')