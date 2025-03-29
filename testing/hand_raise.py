import cv2
import numpy as np

cap = cv2.VideoCapture(0)

print("Raise your hand in front of the webcam to trigger 'Hello 👋'")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip horizontally for natural movement
    frame = cv2.flip(frame, 1)

    # Define region of interest for hand detection (top right box)
    roi = frame[100:300, 350:550]

    # Draw rectangle to show ROI
    cv2.rectangle(frame, (350, 100), (550, 300), (0, 255, 0), 2)

    # Convert ROI to HSV for better skin detection
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create skin mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply some smoothing
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour
        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) > 5000:
            # A large enough contour (like a raised hand)
            cv2.putText(frame, "Hello 👋", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("Hello")

    # Show windows
    cv2.imshow("Webcam Feed", frame)
    cv2.imshow("Hand Mask", mask)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# via chatgpt
