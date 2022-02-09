from typing import ClassVar
import cv2
import mediapipe as mp
import time


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

    
while True:
    success, img = capture.read()
    imgRb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRb)
    # print(results.multi_land_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id==4:
                    cv2.circle(img, (cx, cy), 30, (255,0,255), cv2.FILLED)
                elif id==8:
                    cv2.circle(img, (cx,cy), 30, (255,0,255), cv2.FILLED)    
                elif id==12:
                    cv2.circle(img, (cx,cy), 30, (255,0,255), cv2.FILLED)
                elif id==16:
                    cv2.circle(img, (cx,cy), 30, (255,0,255), cv2.FILLED)    
                elif id==20:
                    cv2.circle(img, (cx,cy), 30, (255,0,255), cv2.FILLED)        
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("image", img)
    cv2.waitKey(1)
