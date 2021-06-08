import cv2

template = cv2.imread('ressource/spike_template.png', cv2.IMREAD_UNCHANGED)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)


async def crop_spike(cap):
    width = 89
    height = 80
    startY = 15
    left = 916
    endY = startY + height
    startX = left
    endX = left + width

    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]

    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)


async def is_spike_planted(cap):
    image = await crop_spike(cap)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    method = cv2.TM_CCOEFF_NORMED
    res = cv2.matchTemplate(image, template, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    max_val_ncc = '{:.3f}'.format(max_val)

    Spike = False

    if float(max_val_ncc) > 0.6:
        Spike = True

    return Spike

if __name__ == '__main__':
    import json

    with open('../ressource/config.json') as config_file:
        settings = json.load(config_file)

    xcap = cv2.VideoCapture(settings['camera_index'], cv2.CAP_DSHOW)
    xcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    xcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    import asyncio

    while True:
        asyncio.run(is_spike_planted(xcap))