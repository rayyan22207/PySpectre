import cv2
import mediapipe as mp

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Define gesture patterns
GESTURES = {
    (0, 0, 0, 0, 0): "Fist",
    (1, 1, 1, 1, 1): "Open Palm",
    (0, 1, 0, 0, 0): "One Finger",
    (0, 1, 1, 0, 0): "Peace ✌️",
    (1, 0, 0, 0, 0): "Thumbs Up 👍",
    (0, 0, 0, 0, 1): "Pinky Up 🧐",
    (0, 0, 1, 0, 0): "giving the bird",
    # Add more if you like
}

def fingers_up(landmarks):
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    fingers = []

    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # Thumb (special case: horizontal)
    if landmarks[4].x > landmarks[3].x:
        fingers.insert(0, 1)
    else:
        fingers.insert(0, 0)

    return tuple(fingers)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_name = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm_list = hand_landmarks.landmark

            finger_pattern = fingers_up(lm_list)

            # Check against gesture dictionary
            gesture_name = GESTURES.get(finger_pattern, "Unknown Gesture")

            # Print and display gesture
            print("Detected:", gesture_name)
            cv2.putText(frame, f"{gesture_name}", (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 255), 3)

    cv2.imshow("Gesture Tracker - Spectra", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
