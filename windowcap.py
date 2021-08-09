#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import win32gui, win32ui, win32con
import numpy as np
import os
from time import time
import cv2 as cv
import pyautogui

class windowcap:

    # properties
    w = 0
    h = 0
    wndw = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name=None,**kwargs):
        #default to desktop if no specified window found
        if window_name==None:
            self.wndw = win32gui.GetDesktopWindow()
        else:
            # find the handle for the window we want to capture
            self.wndw = win32gui.FindWindow(None, window_name)
            if not self.wndw:
                raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.wndw)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # remove window border
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # account for cropping
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screen(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.wndw)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.wndw, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return img
    
    @staticmethod
    def get_windows():
        def winEnumHandler(wndw, ctx):
            if win32gui.IsWindowVisible(wndw):
                print(hex(wndw), win32gui.GetWindowText(wndw)+".")
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

