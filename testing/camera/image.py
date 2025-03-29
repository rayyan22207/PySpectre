import cv2

# Initialize the webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Cannot access the webcam")
    exit()

# Read one frame
ret, frame = cap.read()

if ret:
    # Save the image
    cv2.imwrite("webcam_snapshot.jpg", frame)
    print("📸 Saved webcam image as 'webcam_snapshot.jpg'")
else:
    print("Failed to grab frame")

# Release the camera
cap.release()
cv2.destroyAllWindows()

# code via Chatgpt testing