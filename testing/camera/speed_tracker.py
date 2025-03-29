import cv2
import mediapipe as mp
import math
import time
from datetime import datetime

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Setup video
cap = cv2.VideoCapture(0)

# Logging
log_file = open("velocity_log.txt", "w")
log_file.write("Timestamp\t\tX\tY\tSpeed (m/s)\n")

# Calibration — change this if needed!
PIXELS_PER_METER = 500  # estimate: 500 pixels = 1 meter

# State
prev_x, prev_y = None, None
prev_time = None

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    speed_mps = 0.0
    current_time = time.time()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Track index finger tip (landmark 8)
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw pointer
            cv2.circle(frame, (x, y), 8, (0, 255, 255), -1)

            if prev_x is not None and prev_y is not None:
                dx = x - prev_x
                dy = y - prev_y
                dt = current_time - prev_time if prev_time else 0.01

                distance_pixels = math.hypot(dx, dy)
                speed_mps = (distance_pixels / PIXELS_PER_METER) / dt

            # Update previous values
            prev_x, prev_y = x, y
            prev_time = current_time

            # Show speed on screen
            cv2.putText(frame, f"Speed: {speed_mps:.2f} m/s", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write to log file
            log_file.write(f"{timestamp}\t{x}\t{y}\t{speed_mps:.2f}\n")

    cv2.imshow("Spectra - Hand Velocity Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
log_file.close()
cap.release()
cv2.destroyAllWindows()
