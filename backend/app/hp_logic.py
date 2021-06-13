import cv2
import numpy as np


async def crop_healthbar(left, cap):
    width = 38
    height = 2
    startY = 78
    endY = startY + height
    startX = left
    endX = left + width

    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]

    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)


async def get_healthpercent(player, cap):
    healthBar = await crop_healthbar(player, cap)
    maxvalue = 200
    
    width = 100
    height = healthBar.shape[0] # keep original height
    dim = (width, height)
    
    healthBar = cv2.resize(healthBar, dim) # interpolation = cv2.INTER_AREA

    mask_white = cv2.inRange(healthBar, np.array([240, 240, 240]), np.array([255, 255, 255]))

    #masking red
    # lower boundary RED color range values; Hue (0 - 10)
    lower_red_boundary1 = np.array([0, 0, 20])
    upper_red_boundary1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower_red_boundary2 = np.array([160,0,20])
    upper_red_boundary2 = np.array([179,255,255])

    lower_red = cv2.inRange(healthBar, lower_red_boundary1, upper_red_boundary1)
    upper_red = cv2.inRange(healthBar, lower_red_boundary2, upper_red_boundary2)

    # mask_red = cv2.inRange(healthBar, np.array([0, 0, 0]), np.array([250, 100, 110]))
    mask_red = lower_red + upper_red + cv2.inRange(healthBar, np.array([0, 0, 0]), np.array([250, 100, 110]))

    health_bar = cv2.bitwise_and(healthBar, healthBar, mask=mask_white)
    health_bar_red = cv2.bitwise_and(healthBar, healthBar, mask=mask_red)

    health_bar_red = cv2.cvtColor(health_bar_red, cv2.COLOR_BGR2GRAY)
    health_bar = cv2.cvtColor(health_bar, cv2.COLOR_BGR2GRAY)

    hbpixels = health_bar.reshape(-1, 1)
    lhbpixels = health_bar_red.reshape(-1, 1)

    hp = 0
    pixels_found = False

    for pixel in hbpixels:
        if pixel[0] >= 240:
            hp += 1
            pixels_found = True

    for pixel in lhbpixels:
        if not pixels_found:
            if pixel[0] >= 70:
                hp += 1

    health_percent = hp / maxvalue * 100

    if health_percent > 100:
        health_percent = 100

    # health_bar = cv2.resize(healthBar, (460, 120))
    # cv2.imshow(str(player), health_bar)
    
    # cv2.waitKey(0)

    return round(health_percent)


if __name__ == '__main__':
    import json

    with open('../ressource/config.json') as config_file:
        settings = json.load(config_file)

    xcap = cv2.VideoCapture(settings['camera_index'], cv2.CAP_DSHOW)
    xcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    xcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    import asyncio

    # while True:
    #     asyncio.run(get_healthpercent(settings['team_1'][f'player_4_position'], xcap))

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    print(asyncio.run(get_healthpercent(settings['team_1'][f'player_4_position'], xcap)))
