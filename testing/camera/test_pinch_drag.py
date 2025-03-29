import cv2
import mediapipe as mp
import math

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# Initial object position
obj_x, obj_y = 300, 300
radius = 40
dragging = False

def get_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    pinch_detected = False
    cursor_x, cursor_y = obj_x, obj_y

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of thumb tip (4) and index tip (8)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_pos = (int(index_tip.x * w), int(index_tip.y * h))

            # Draw points
            cv2.circle(frame, thumb_pos, 10, (255, 0, 0), -1)
            cv2.circle(frame, index_pos, 10, (0, 255, 0), -1)

            # Check distance between fingers (pinch)
            distance = get_distance(thumb_pos, index_pos)
            if distance < 40:  # adjust sensitivity if needed
                pinch_detected = True
                cursor_x, cursor_y = ((thumb_pos[0] + index_pos[0]) // 2,
                                      (thumb_pos[1] + index_pos[1]) // 2)
                cv2.putText(frame, "Pinching 👌", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    # If pinching and near the object, start dragging
    if pinch_detected:
        if get_distance((cursor_x, cursor_y), (obj_x, obj_y)) < radius + 30 or dragging:
            dragging = True
            obj_x, obj_y = cursor_x, cursor_y
    else:
        dragging = False

    # Draw draggable object
    cv2.circle(frame, (obj_x, obj_y), radius, (0, 255, 255), -1)
    cv2.putText(frame, "Drag the ball by pinching!", (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Spectra - Pinch and Drag", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
