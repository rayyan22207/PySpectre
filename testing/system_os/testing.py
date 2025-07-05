import cv2
import numpy as np
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize camera
cap = cv2.VideoCapture(0)

# MediaPipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Pycaw volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]  # Usually -65.25 to 0.0
current_vol_scalar = volume.GetMasterVolumeLevelScalar()  # 0.0 to 1.0
print(f"Current Volume: {int(current_vol_scalar * 100)}%")
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if lmList:
        # Thumb tip = 4, Index finger tip = 8
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Draw line between them
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Convert length to volume
        vol = int(np.interp(length, [20, 200], [volMin, volMax]))
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)
        # Draw volume bar
        vol_bar = np.interp(length, [20, 200], [400, 150])
        cv2.rectangle(img, (50, 150), (85, 400), (0,255,0), 2)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0,255,0), cv2.FILLED)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
