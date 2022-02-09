import cv2
import mediapipe as mp
import time
import numpy as nmp
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


##############################
wCam, hCam = 640, 480
##############################


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0   
detector = htm.handDetector(detectionCon = 0.5) 

#change the volume based on the estimated eucledian length(import the pyCaw package)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()#value range from -65 to 0 as maximum, ignore the 0.03125 case((-65.25, 0.0, 0.03125))
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
vol = 0
volPer = 0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
      # print(lmList[4],lmList[8])

      x1, y1 = lmList[4][1], lmList[4][2]
      x2, y2 = lmList[8][1], lmList[8][2]
      cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

      cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
      cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)        
      cv2.line(img, (x1, y1),(x2, y2), (255,0,255), 5) 
      # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

      length = math.hypot(x2 - x1, y2 - y1)#euclidian distance(d) calc.
      # print(length)

      #1.Hand range from 50(as minimum) - 300(as maximum)
      #2.Volume range from -65(as minimum) - 0(as maximum)
      #3.Convert From no.1 Value range to no.2 Value range
      vol = nmp.interp(length,[50,300],[minVol,maxVol])
      volBar = nmp.interp(length,[50,300],[400,150])
      volPer = nmp.interp(length, [50,300], [0,100])
      print(int(length),vol)
      volume.SetMasterVolumeLevel(vol, None)

      if length < 50:#if eucledian less than 50
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)#3 as a replacement for cv2.FILLED cuz we dont wanna to fill the rectangle
    cv2.rectangle(img, (50,int(volBar)), (85,400), (0,255,0), cv2.FILLED) 
    cv2.putText(img, f'Vol: {int(volPer)}%',(40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 3) 
    
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)     

    cv2.imshow("image", img)
    cv2.waitKey(1)  

