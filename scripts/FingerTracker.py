import cv2
import mediapipe as mp
import os
import numpy as np

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))    

while True:
    success, img = cap.read()   
    h, w, c = overlayList[0].shape
    img = np.zeros[0:200, 0:200] = overlayList[0]
    cv2.imshow("Image", img)
    cv2.waitKey(1)

