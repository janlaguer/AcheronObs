import cv2
import numpy as np
from pytesseract import image_to_string
import asyncio

async def clean_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
    frame = cv2.bilateralFilter(frame, 9, 75, 75)
    frame = cv2.threshold(frame, 240, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((4, 4), np.uint8)
    frame = cv2.dilate(frame, kernel, iterations=1)
    frame = cv2.erode(frame, kernel, iterations=1)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    # frame = cv2.Canny(frame, 50, 100)

    return frame


async def crop_score(left, cap):
    width = 30
    height = 30
    startY = 38
    endY = startY + height
    startX = left
    endX = left + width

    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]

    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)


async def get_score(team, cap) -> str:
    loop = asyncio.get_event_loop()

    frame = await crop_score(team, cap)
    frame = await clean_frame(frame)

    custom_config = r'-c tessedit_char_whitelist=0123456789'
    score = await loop.run_in_executor(None, lambda: image_to_string(frame, config=custom_config))
    score = score.replace('\n', '').replace('\f', '')

    if not score:
        frame = await crop_score(team, cap)
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789 outputbase digit'
        score = await loop.run_in_executor(None, lambda: image_to_string(frame, config=custom_config))
        score = score.replace('\n', '').replace('\f', '')
        if not score:
            score = "0"

    # cv2.imshow("Score", frame)
    # cv2.waitKey(0)

    return score


if __name__ == '__main__':
    import json

    with open('../ressource/config.json') as config_file:
        settings = json.load(config_file)

    xcap = cv2.VideoCapture(settings['camera_index'], cv2.CAP_DSHOW)
    xcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    xcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    import asyncio

    while True:
        asyncio.run(get_score(settings['score_left_position'], xcap))
