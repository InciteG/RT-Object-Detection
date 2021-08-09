#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import win32gui, win32ui, win32con
import numpy as np
import os
from time import time
import cv2 
import pyautogui

def target_acq(in_path, img_test,match=cv2.TM_CCOEFF_NORMED,threshold = 0.7,debug_mode=None, **kwargs):
    target= cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    target= cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    target_w = target.shape[1]
    target_h = target.shape[0]
    result = cv2.matchTemplate(img_test,target,match)
    if match in [cv2.TM_SQDIFF_NORMED,cv2.TM_SQDIFF]:
        locations = np.where(result<threshold)
        locations = list(zip(*locations[::-1]))
    else:
        locations = np.where(result>=threshold)
        locations = list(zip(*locations[::-1]))
    
    rectangles = []
    for i in locations:
        rect = [int(i[0]),int(i[1]),target_w,target_h]
        rectangles.append(rect)
        rectangles.append(rect)
    rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1,eps=0.5)
    
    points = []
    if len(rectangles):
        line_color = (0,255,0)
        line_type = cv2.LINE_4
        marker_color = (255,0,255)
        marker_type = cv2.MARKER_CROSS
        for (x,y,w,h) in rectangles:
            center_x = x+int(w/2)
            center_y = y+int(h/2)
            
            points.append((center_x,center_y))
        if debug_mode =='rectangles':
            top_left = (x,y)
            bottom_right = (x+w,y+h)
            cv2.rectangle(img_test,top_left,bottom_right, color=line_color,lineType=line_type, thickness=2)
        elif debug_mode==points:
            cv2.drawMarker(img_test, (center_x,center_y),color=marker_color,markerType=marker_type,markerSize=40,thickness=2)
        
    if debug_mode:
        cv2.imshow('Matches', img_test)
        


# In[ ]:




