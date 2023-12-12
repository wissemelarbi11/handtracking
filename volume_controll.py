import cv2
import mediapipe as mp
import pyautogui
x1 = y1 = x2 = y2 = 0

webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    success, frame = webcam.read()
    frame = cv2.flip(frame,1)

    if not success:
        print("Failed to capture frame")
        break

    frame_height, frame_width, _ = frame.shape  # Fix: Remove the parentheses

    cv2.imshow("Hand volume control using python", frame)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get hand landmarks
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand_landmarks in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand_landmarks)
            landmarks = hand_landmarks.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame,center=(x,y), radius=8,color=(0, 255, 255),thickness=3)
                    x1 = x
                    y1 = y

                if id == 4:
                    cv2.circle(img=frame,center=(x,y), radius=8,color=(0, 255, 255),thickness=3)
                    x2 = x
                    y2 = y
                dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4

                cv2.line(frame, (x1, y1), (x2, y2), color=(0,255,255), thickness=5)
                if dist > 50 :
                    pyautogui.press("volumeup")
                else:
                    pyautogui.press("volumedown")
    cv2.imshow("Hand volume control using python", frame)

    try:
        # Wait for a key event for 10 milliseconds
        key = cv2.waitKey(10)

        # Check if any key is pressed
        if key != -1:
            break

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to exit the loop
        break

# Release the webcam and close the OpenCV window
webcam.release()
cv2.destroyAllWindows()
my_hands.close()

