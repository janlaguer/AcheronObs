import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import mss
import time
import timeit
import threading
from collections import defaultdict 
import sys
import json
import requests
from collections import deque
from termcolor import colored
import pytesseract
from pytesseract import Output

# Globals
health_percentage = 100
maxvalue = 70
# TEAM1 LEFT POSITION VALUES (1920*1080)
player1 = 443
player2 = 509
player3 = 575
player4 = 641
player5 = 707
# TEAM2 LEFT POSITION VALUES (1920*1080)
player6 = 1168
player7 = 1234
player8 = 1300
player9 = 1366
player0 = 1432
teamleftScore = 796
teamrightScore = 1087
pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\Tesseract-OCR\tesseract.exe'
VERBOSE = False
VERBOSETESSERACT = False
DISPLAY = False


def grab_screen(left):
    width  = 46
    height = 12
    startY = 73
    endY = startY + height
    startX = left
    endX = left + width
    camera_index = 0
    e1 = cv2.getTickCount()
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()
    frame = frame[startY:endY,startX:endX]
    e2 = cv2.getTickCount()
    timec = (e2 - e1)/ cv2.getTickFrequency()
    func_name = sys._getframe().f_code.co_name
    print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

def grab_time():
    width = 88
    height = 50
    startY = 25
    left = 910
    
    endY = startY + height
    startX = left
    endX = left + width

    camera_index = 0
    e1 = cv2.getTickCount()
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()
    frame = frame[startY:endY,startX:endX]
    e2 = cv2.getTickCount()
    timec = (e2 - e1)/ cv2.getTickFrequency()
    func_name = sys._getframe().f_code.co_name
    print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))
    
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

def grab_score(left):
    width = 46
    height = 43
    startY = 30
    
    endY = startY + height
    startX = left
    endX = left + width
    e1 = cv2.getTickCount()
    camera_index = 0
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()
    frame = frame[startY:endY,startX:endX]
    
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
    hwin = win32gui.GetDesktopWindow()
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    e2 = cv2.getTickCount()
    timec = (e2 - e1)/ cv2.getTickFrequency()
    func_name = sys._getframe().f_code.co_name
    print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def getTime():
    e1 = cv2.getTickCount()
    frame = grab_time()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=1)
    frame = cv2.erode(frame, kernel, iterations=1)
    frame = cv2.threshold(cv2.bilateralFilter(frame, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789:.'
    roundtime = pytesseract.image_to_string(frame, config=custom_config)
    if VERBOSETESSERACT == True:
        print(roundtime)
    cv2.destroyAllWindows()
    e2 = cv2.getTickCount()
    timec = (e2 - e1)/ cv2.getTickFrequency()
    func_name = sys._getframe().f_code.co_name
    print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))
    return roundtime

def getScore(teamscore):
    e1 = cv2.getTickCount()
    frame = grab_score(teamscore)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    #frame = cv2.dilate(frame, kernel, iterations=1)
    #frame = cv2.erode(frame, kernel, iterations=1)
    #frame = cv2.threshold(cv2.bilateralFilter(frame, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    custom_config = r'--oem 3 --psm 7 outputbase digits'
    score = pytesseract.image_to_string(frame, config=custom_config)
    if VERBOSETESSERACT == True:
        print(score)
    cv2.destroyAllWindows()
    e2 = cv2.getTickCount()
    timec = (e2 - e1)/ cv2.getTickFrequency()
    func_name = sys._getframe().f_code.co_name
    print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))
    return int(score)

def getplayer(player):
        e1 = cv2.getTickCount()
        frame_ring_buffer = deque([], 3)
        screengrab = grab_screen(player)
        frame_ring_buffer.append(screengrab)
        frame_ring_buffer.append(screengrab)
        frame_ring_buffer.append(screengrab)

        # 3 frame de buffer
        frame1 = cv2.cvtColor(np.array(frame_ring_buffer[0]), cv2.COLOR_RGB2BGR)
        if(len(frame_ring_buffer) == 3):
            frame2 = cv2.cvtColor(np.array(frame_ring_buffer[1]), cv2.COLOR_RGB2BGR)
            frame3 = cv2.cvtColor(np.array(frame_ring_buffer[2]), cv2.COLOR_RGB2BGR)
            frame2 = cv2.max(frame1, frame2)
            health_bar = cv2.max(frame2, frame3)
        else:
            print(colored("WARNING: Frame buffer < 3", "yellow"))
            health_bar = frame1

        #health_bar = cv2.bilateralFilter(health_bar, 3, 2, 2)
        
        # Masque blanc
        mask1 = cv2.inRange(health_bar, np.array([240, 240, 240]), np.array([255, 255, 255]))

        # Conversion bgr => hsv
        health_bar_hsv = cv2.cvtColor(health_bar, cv2.COLOR_BGR2HSV)
        health_bar_hsv  = cv2.dilate(health_bar_hsv, None, iterations=1)
        health_bar_hsv  = cv2.erode(health_bar_hsv, None, iterations=1)


        lower_red1 = np.array([170, 110, 85])
        upper_red1 = np.array([180, 255, 255])
        lower_red2 = np.array([0, 110, 85])
        upper_red2 = np.array([10, 255, 255])

        # Masques rouge
        mask2 = cv2.inRange(health_bar_hsv, lower_red1, upper_red1)
        mask3 = cv2.inRange(health_bar_hsv, lower_red2, upper_red2)

        # Je cherche sur mon masque et par sur mon image parce que ça marche bien
        hsvBar = cv2.bitwise_or(mask2, mask3)

        health_bar = cv2.bitwise_and(health_bar, health_bar, mask = mask1)
        health_bar = cv2.cvtColor(health_bar, cv2.COLOR_BGR2GRAY)

        hbpixels = health_bar.reshape(-1,3)
        lhbpixels = hsvBar.reshape(-1,3)
        pv = 0
        foundpixels = False
        for hbpixel in hbpixels:

            if hbpixel[0] >= 240 and hbpixel[1] >= 240 and hbpixel[2] >= 240:
               pv += 1
               foundpixels = True

        for lhbpixel in lhbpixels:
            if (foundpixels == False): 
                    if lhbpixel[0] >= 240 and lhbpixel[1] >= 240 and lhbpixel[2] >= 240:
                        pv += 1

        health_percent = pv/maxvalue * 100
        if (health_percent > 100):
            health_percent = 100

        # Buffer de 3 mesures
        health_percent_buffer = deque([], 3)

        health_percent_buffer.append(health_percent)
        health_percent_buffer.append(health_percent)
        health_percent_buffer.append(health_percent)

        health_percent = round(np.mean(health_percent_buffer))
        if VERBOSE == True:
            print('Detected health : ' + str(health_percent))

        if DISPLAY == True :
            health_bar = cv2.resize(health_bar, (460, 120))
            cv2.imshow(str(player),health_bar)
            hsvBar = cv2.resize(hsvBar, (460, 120))
            cv2.imshow(str(player + 1),hsvBar)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        e2 = cv2.getTickCount()
        timec = (e2 - e1)/ cv2.getTickFrequency()
        func_name = sys._getframe().f_code.co_name
        print('Execution Time : ' + str(round(timec,2)) +" --- "+ str(func_name))
        return health_percent

def start(ENABLE,POST):
    useoptimized = cv2.useOptimized()
    print (useoptimized)
    while ENABLE == True:
        tic = time.perf_counter()
        pv_player = []
        pv_player.append(getplayer(player1))
        pv_player.append(getplayer(player2))
        pv_player.append(getplayer(player3))
        pv_player.append(getplayer(player4))
        pv_player.append(getplayer(player5))
        pv_player.append(getplayer(player6))
        pv_player.append(getplayer(player7))
        pv_player.append(getplayer(player8))
        pv_player.append(getplayer(player9))
        pv_player.append(getplayer(player0))
        roundtimer = getTime()
        scoreLeft = getScore(teamleftScore)
        scoreRight = getScore(teamrightScore)

        ## FIX FOR THE HUD RITO PLEASE FIX
        if scoreLeft + scoreRight >= 12:
            scoreLeft = getScore(teamrightScore)
            scoreRight = getScore(teamleftScore)
        toc = time.perf_counter()
        print(f"Total execution time : {toc - tic:0.4f} seconds")
        if POST == True:
            with requests.get('http://localhost:7000/api/123') as api:
                data = api.json()
                data["team1"]["players"][0]["hp"] = str(pv_player[0])
                data["team1"]["players"][1]["hp"] = str(pv_player[1])
                data["team1"]["players"][2]["hp"] = str(pv_player[2])
                data["team1"]["players"][3]["hp"] = str(pv_player[3])
                data["team1"]["players"][4]["hp"] = str(pv_player[4])
                data["team2"]["players"][0]["hp"] = str(pv_player[5])
                data["team2"]["players"][1]["hp"] = str(pv_player[6])
                data["team2"]["players"][2]["hp"] = str(pv_player[7])
                data["team2"]["players"][3]["hp"] = str(pv_player[8])
                data["team2"]["players"][4]["hp"] = str(pv_player[9])
                data["team1"]["roundscore"] = str(scoreLeft)
                data["team2"]["roundscore"] = str(scoreRight)
                data["roundtime"] = str(roundtimer)

                #jsonData = json.dumps(data)
                #print(jsonData)

                response = requests.post('http://localhost:7000/api/123', json=data)

                print("Status code: ", response.status_code)

start(ENABLE=True,POST=False)