import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access the webcam")
    exit()

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Live Webcam Feed", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# code via Chatgpt testing