# Virtual Mouse with Hand Tracking

This project implements a virtual mouse using hand gestures and webcam input. By utilizing **OpenCV**, **MediaPipe**, and **Autopy**, you can control your computer's mouse using simple hand movements detected through the camera.

## Features
- **Mouse Movement**: Control the mouse pointer by moving your index finger in front of the camera.
- **Clicking**: Perform a click action by bringing your index and middle fingers together.
- **Smooth Movement**: The pointer movement is smoothened to make the virtual mouse feel more natural.
  
## Demo
![Demo](demo.gif)  *(Add a demo GIF or image of your virtual mouse in action)*

## Installation

### Requirements
- **Python 3.x**
- The following Python libraries are required:
  ```bash
  pip install opencv-python mediapipe autopy numpy
  ```

### Clone the repository
```bash
git clone https://github.com/yourusername/VirtualMouseHandTracking.git
cd VirtualMouseHandTracking
```

## Usage

1. **Run the Python Script**:
    ```bash
    python VirtualMouse.py
    ```

2. **Control the mouse**:
   - Move the index finger to control the mouse pointer.
   - Bring the index and middle fingers together to click.
   
3. Press `q` to quit the program.

## Code Structure

- **`VirtualMouse.py`**: The main script that handles webcam input, hand tracking, and mouse control.
- **`HandTrackingModule.py`**: A custom module that uses MediaPipe to detect hand landmarks and provide useful functions like detecting which fingers are up and calculating the distance between fingertips.

## How It Works
- The webcam captures video frames.
- The **MediaPipe** library detects hand landmarks in real-time.
- The position of the index finger is mapped to the screen, controlling the mouse movement.
- Clicking is triggered when the index and middle fingers are brought close together.

## Customization
You can customize the following parameters in the code:
- **Frame Reduction (`frameR`)**: Adjust the area within which hand movements are detected.
- **Smoothening (`smoothening`)**: Controls how smooth the mouse movement is.
  
## To-Do
- [ ] Add right-click functionality.
- [ ] Implement scrolling gestures.
- [ ] Improve gesture detection accuracy.

## Contributing
Feel free to open issues or create pull requests if you want to contribute to this project.

## License

---

With this **README**, users and developers can easily understand the project, install dependencies, and start using the virtual mouse!
