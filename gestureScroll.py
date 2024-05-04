from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui


# Initialize the webcam to capture video
# The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
cap = cv2.VideoCapture(0)

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()

    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        #print(f'H1 = {fingers1}', end="\r")  # Print the count of fingers that are up
        if fingers1[0]:#伸拇指往下翻
            pyautogui.scroll(-200);
        else:
            if fingers1[1]:#伸食指往上翻
                pyautogui.scroll(200);

        # Check if a second hand is detected
        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detector.fingersUp(hand2)
            if fingers2[0]:#伸拇指往下翻
                pyautogui.scroll(-200);
            else:
                if fingers2[1]:#伸食指往上翻
                    pyautogui.scroll(200);            
            if fingers1[0] and fingers1[1] and fingers1[2] and fingers1[3] and fingers1[4] and \
                fingers2[0] and fingers2[1] and fingers2[2] and fingers2[3] and fingers2[4] :
                print("gesture exit")
                break;

    # Display the image in a window
    #cv2.imshow("Image", img)

    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
