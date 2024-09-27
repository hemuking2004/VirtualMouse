import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

# Configurable parameters
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction to create interactive region
smoothening = 7

# Variables for previous and current positions
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Variables for drag and drop
dragging = False
right_click_time = 0  # Debounce for right-click

# Capture from primary camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Width
cap.set(4, hCam)  # Height

# Create a hand detector object
detector = htm.handDetector(maxHands=1)

# Get screen width and height for mouse control
wScr, hScr = autopy.screen.size()


def perform_right_click():
    """Performs a right mouse click."""
    autopy.mouse.click(autopy.mouse.Button.RIGHT)


def perform_left_click():
    """Performs a left mouse click."""
    autopy.mouse.click(autopy.mouse.Button.LEFT)


def perform_minimize():
    """Minimizes the current window."""
    autopy.key.tap(autopy.key.Code.DOWN_ARROW, [autopy.key.Modifier.META])


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
        x_thumb, y_thumb = lmList[4][1:]  # Thumb tip
        x_pinky, y_pinky = lmList[20][1:]  # Pinky finger tip

    # 3. Check which fingers are up
    fingers = detector.fingersUp()

    # Create an interactive area rectangle
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Moving Mode (only index finger up)
    if len(fingers) >= 2 and fingers[1] == 1 and fingers[2] == 0:
        # Convert coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        # Smoothen the mouse movement
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        # Move the mouse
        autopy.mouse.move(wScr - clocX, clocY)
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 5. Drag and Drop Mode (thumb and index fingers together)
    if len(fingers) >= 2 and fingers[1] == 1 and fingers[0] == 1:  # Thumb and index finger up
        length, img, lineInfo = detector.findDistance(4, 8, img)  # Thumb (4) and Index (8)

        # Check distance between thumb and index for drag
        if length < 40 and not dragging:
            autopy.mouse.toggle(down=True)  # Start dragging
            dragging = True
            cv2.putText(img, "Dragging", (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif length >= 40 and dragging:
            autopy.mouse.toggle(down=False)  # Release drag
            dragging = False
            cv2.putText(img, "Released", (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    # 6. Clicking Mode (middle finger up for left click)
    if len(fingers) >= 3 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            perform_left_click()

    # 7. Right-Click Mode (pinky finger up for right click)
    current_time = time.time()
    if len(fingers) >= 2 and fingers[4] == 1 and fingers[1] == 1:  # Pinky and index fingers up
        if current_time - right_click_time > 1:  # Debounce right-click (1 second delay)
            perform_right_click()
            right_click_time = current_time  # Update last right-click time
            cv2.putText(img, "Right Click", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # 8. Multi-finger Window Management (Three fingers up to minimize window)
    if fingers == [1, 1, 1, 0, 0]:  # Three fingers up
        perform_minimize()
        time.sleep(0.1)  # 100 ms delay

    # 9. Frame Rate Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on screen
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 10. Display the image
    cv2.imshow("Virtual Mouse", img)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
