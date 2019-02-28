# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 09:06:06 2018

@author: Ian
"""
import requests
import cv2
import numpy as np
import json


def triggered(message):
    url = 'https://bosch-ville-api.unificationengine.com/v1/message/send'
    api_token = 'Y2gmZGV2aWNlX3R5cGU9WERJ'
    headers = {'Content-Type': 'application/json', 'Authorization': api_token}
    body = {"phone_number": "+6598287932","message": message}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    
    
#this is the cascade we just made. Call what you want
trash_cascade = cv2.CascadeClassifier('cascade.xml')

cap = cv2.VideoCapture(0)

while True:
    
    ret, img = cap.read()
    
    if ret is True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else: 
        print("ret is False")
        
    trash = trash_cascade.detectMultiScale(gray, 20,20)

    for (x,y,w,h) in trash:
        cv2.rectangle(img ,(x,y),(x+w,y+h),(255,255,0),2)
        font = cv2. FONT_HERSHEY_SIMPLEX
        cv2.putText(img, 'Trash', (w-x,y-h), font, 0.5,(255,255,0), 2, cv2.LINE_AA)
    
    triggered("Trash build up is too much. Help service hotline activated!")
        
    cv2.imshow('gray', gray)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()