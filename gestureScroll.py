#coding=utf-8
import cv2
import pyautogui
import numpy as np
import time
import math
import mediapipe as mp
class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(self.results.multi_handedness)  # 获取检测结果中的左右手标签并打印

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []
        # 大拇指
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其余手指
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)        # 检测手势并画上骨架信息

        lmList = detector.findPosition(img)  # 获取得到坐标点的列表




        # k = cv2.waitKey(1) & 0xFF  # 判断按键



        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, 'fps:' + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

##############################
wCam, hCam = 1000, 1000
frameR = 100
smoothening = 5
##############################
cap = cv2.VideoCapture(0)  # 若使用笔记本自带摄像头则编号为0  若使用外接摄像头 则更改为1或其他编号
#设置摄像头的呈现画面的宽高
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = handDetector()
wScr, hScr = pyautogui.size()
# print(wScr, hScr)

while True:
    success, img = cap.read()
    # 1. 检测手部 得到手指关键点坐标
    img = detector.findHands(img)
    #cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 255, 0), 2,  cv2.FONT_HERSHEY_PLAIN)
    lmList = detector.findPosition(img, draw=False)




    # k = cv2.waitKey() & 0xFF  # 判断按键

    # 2. 判断食指和中指是否伸出
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        print(fingers,end='\r')
        if fingers[0]:#伸拇指往下翻
            pyautogui.scroll(-200);
        else:
            if fingers[1]:#伸食指往上翻
                pyautogui.scroll(200);
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            print("\ngesture exit")
            break
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps:{int(fps)}', (15, 25),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.imshow("Gesture Scroll", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nkey exit")
        break
#释放摄像头
cap.release()
#释放内存
cv2.destroyAllWindows()
