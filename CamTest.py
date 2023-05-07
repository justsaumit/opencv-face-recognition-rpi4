import cv2
from picamera2 import Picamera2

# Create an instance of the PiCamera2 object
cam = Picamera2()

# Set the resolution of the camera preview
cam.preview_configuration.main.size = (1280,720)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

# While loop to continuously capture frames from camera
while True:
    # Capture a frame from the camera
    frame=cam.capture_array()

    # Convert frame from BGR to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the original frame and grayscale frame
    cv2.imshow('OriginalBGR', frame)
    cv2.imshow('Grayscale', gray)
    
    # Wait for 30 milliseconds for a key event (extract sigfigs) and exit if 'ESC' or 'q' is pressed
    key = cv2.waitKey(30) & 0xff
    #Checking keycode
    if key == 27:  # ESCAPE key
        break
    elif key == 113:  # q key
        break

# Release the camera and close all windows
cam.release()
cv2.destroyAllWindows()
