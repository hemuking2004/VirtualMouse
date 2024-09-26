import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

# Configurable parameters
wCam, hCam = 640, 480
frameR = 70  # Frame Reduction
smoothening = 7

# Previous and current positions
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Capture from primary camera
cap = cv2.VideoCapture(0)  # Changed to 0 to ensure the primary camera is used
cap.set(3, wCam) #width
cap.set(4, hCam) #height

# Create a hand detector object
detector = htm.handDetector(maxHands=1)

# Get screen width and height
wScr, hScr = autopy.screen.size()

def perform_right_click():
    autopy.mouse.click(autopy.mouse.Button.RIGHT)

def perform_left_click():
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def scroll_screen(scroll_amount):
    autopy.scroll(scroll_amount)

prev_y = None

while True:
    # 1. Capture frame
    success, img = cap.read()
    if not success:
        continue

    # 2. Detect hand landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        x_thumb, y_thumb = lmList[4][1:]  # Thumb tip

    # 3. Check which fingers are up
    fingers = detector.fingersUp()

    # Create a rectangle for interactive area
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Moving Mode (only index finger up)
    if len(fingers) >= 2 and fingers[1] == 1 and fingers[2] == 0:
        # 5. Convert coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        # 6. Smoothen the values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # 7. Move the mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 8. Clicking Mode (middle finger up for left click)
    if len(fingers) >= 3 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
        # 9. Find distance between index and middle finger
        length, img, lineInfo = detector.findDistance(8, 12, img)

        # 10. Perform click if the distance is less than 40 pixels
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            perform_left_click()

    # 11. Right-Click Mode (thumb and index fingers up)
    if len(fingers) >= 2 and fingers[1] == 1 and fingers[0] == 1:
        # 12. Perform right click
        perform_right_click()
        cv2.putText(img, "Right Click", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 13. Scrolling Mode (thumb and index fingers in contact)
    if len(fingers) >= 2 and fingers[1] == 1 and fingers[0] == 1 and detector.findDistance(4, 8, img)[0] < 30:
        if prev_y is None:
            prev_y = y1
        # 14. Determine scrolling direction
        if y1 < prev_y:
            scroll_screen(3)  # Scroll up
        elif y1 > prev_y:
            scroll_screen(-3)  # Scroll down
        prev_y = y1

    # 15. Frame Rate Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on screen
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 16. Display
    cv2.imshow("Virtual Mouse", img)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
