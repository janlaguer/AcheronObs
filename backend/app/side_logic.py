import cv2
import numpy as np

async def crop_sidebox(cap):
    width = 20
    height = 40
    startY = 30
    endY = startY + height
    startX = 758
    endX = 758 + width

    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]

    return frame

async def is_side(xcap):
    old_frame = await crop_sidebox(xcap)
    hsv = cv2.cvtColor(old_frame, cv2.COLOR_BGR2HSV)

    # set low and high boundery colors for hsv color space
    low = np.array([71, 102, 62])
    high = np.array([95, 151, 170])

    mask = cv2.inRange(hsv, low, high)
    if np.sum(mask) > 0:
        return 0 # this means they're defending
    else:
        return 1 # this means they're attacking
    

if __name__ == '__main__':
    width = 20
    height = 40
    startY = 30
    endY = startY + height
    startX = 758
    endX = 758 + width

    xcap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    xcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    xcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    while True:
        ret, frame = xcap.read()
        frame = frame[startY:endY, startX:endX]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low = np.array([71, 102, 62])
        high = np.array([95, 151, 170])

        mask = cv2.inRange(hsv, low, high)
        if np.sum(mask) > 0:
            print('defender')
        else:
            print('attacker')
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    xcap.release()
    cv2.destroyAllWindows