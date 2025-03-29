import cv2
import mediapipe as mp
import math

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)

cap = cv2.VideoCapture(0)

# Object properties
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

    cursor_x, cursor_y = obj_x, obj_y
    pinch_detected = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index and thumb tip landmarks
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Convert to pixel coordinates
            index_pos = (int(index_tip.x * w), int(index_tip.y * h))
            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            # Calculate pinch distance
            distance = get_distance(index_pos, thumb_pos)

            # Draw landmarks
            cv2.circle(frame, index_pos, 8, (0, 255, 0), -1)
            cv2.circle(frame, thumb_pos, 8, (255, 0, 0), -1)
            cv2.line(frame, index_pos, thumb_pos, (255, 255, 0), 2)

            # Detect pinch
            if distance < 40:  # threshold (pixels)
                pinch_detected = True
                cursor_x, cursor_y = ((index_pos[0] + thumb_pos[0]) // 2,
                                      (index_pos[1] + thumb_pos[1]) // 2)
                cv2.putText(frame, "Pinching 👌", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    # Check if pinch is near the object or already dragging
    if pinch_detected and (get_distance((cursor_x, cursor_y), (obj_x, obj_y)) < radius + 30 or dragging):
        dragging = True
        obj_x, obj_y = cursor_x, cursor_y
    else:
        dragging = False

    # Draw the draggable object
    cv2.circle(frame, (obj_x, obj_y), radius, (0, 255, 255), -1)
    cv2.putText(frame, "Pinch to grab & move the ball", (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 255), 1)

    cv2.imshow("Spectra - Pinch and Drag", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
