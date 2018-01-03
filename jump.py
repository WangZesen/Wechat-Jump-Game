import cv2, os, time, random
import numpy as np

def getNextPos(CP, canny):
    for i in range(960):
        for j in range(540):
            if canny[i + 200][j] != 0 and (j < CP - 25 or j > CP + 25):
                pos = j
                for k in reversed(range(540)):
                    if canny[i + 200][k] != 0 and (k < CP - 25 or k > CP + 25):
                       pos = (j + k) // 2
                       break
                cv2.line(canny, (pos, 0), (pos, 959), (255), 2)
                return pos

def colorDist(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
                
def getCurrentPos(img):
    for i in range(200, 760):
        for j in range(540):
            if colorDist(img[i][j], [125, 77, 85]) < 20:
                cv2.line(img, (j, 0), (j, 959), (255, 255, 255), 2) 
                #cv2.line(img, (j - 25, 0), (j - 25, 959), (255, 255, 255), 2) 
                #cv2.line(img, (j + 25, 0), (j + 25, 959), (255, 255, 255), 2)
                return j

while True:
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png")
    img = cv2.imread("screen.png", 3)
    img = cv2.resize(img, (540, 960))
    print (img[475][168])
    img1 = cv2.resize(cv2.imread("screen.png", 0), (540, 960))
    canny = cv2.Canny(img1, 0, 10)
    k = 714 / 225
    currentPos = getCurrentPos(img)
    nextPos = getNextPos(currentPos, canny)
    cv2.imshow('next pos', canny)
    cv2.waitKey(1000)
    cv2.imshow('current pos', img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    pressTime = int(k * abs(currentPos - nextPos))
    print (currentPos, nextPos, pressTime)
    os.system("adb shell input swipe 500 500 500 500 " + str(pressTime))
    time.sleep(1.5 + random.uniform(0, 0.5))