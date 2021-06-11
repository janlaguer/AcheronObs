import cv2


def crop_ultimatebar(left, cap):
    width = 40
    height = 6
    startY = 20
    endY = startY + height
    startX = left
    endX = left + width

    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]

    return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)


def is_ultimate_up(player, cap) -> bool:
    ultimate_bar = crop_ultimatebar(player, cap)
    ultimate_bar = cv2.cvtColor(ultimate_bar, cv2.COLOR_BGR2GRAY)

    ult_pixels = ultimate_bar.reshape(-1, 1)

    ultimate_status = False
    threshold = 0

    for pixel in ult_pixels:
        if pixel[0] >= 90:
            threshold += 1
            if threshold >= 20:
                ultimate_status = True

    return ultimate_status
