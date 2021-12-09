import cv2
import json

with open('backendv2/ressource/config.json') as config_file:
    settings = json.load(config_file)

xcap = cv2.VideoCapture(settings['camera_index'], cv2.CAP_DSHOW)
xcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
xcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = xcap.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
xcap.release()
cv2.destroyAllWindows