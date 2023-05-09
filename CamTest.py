import cv2
import time
from picamera2 import Picamera2

# Create an instance of the PiCamera2 object
cam = Picamera2()
#Parameters
fps=0
pos=(30,60) #top-left
font=cv2.FONT_HERSHEY_COMPLEX
height=1.5 #font_scale
color=(0,0,255) #text color, OpenCV operates in BGR- RED
weight=3   #font-thickness

# Set the resolution of the camera preview
cam.preview_configuration.main.size = (640, 360)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate=30
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

# While loop to continuously capture frames from camera
while True:
    tStart=time.time()

    # Capture a frame from the camera
    frame=cam.capture_array()
    #Display FPS
    cv2.putText(frame,str(round(fps))+' FPS',pos,font,height,color,weight)
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

    #calculate fps
    tEnd=time.time()
    # time between two epochs
    looptime=tEnd-tStart
    fps=1/looptime

# Release the camera and close all windows
cam.stop()
cv2.destroyAllWindows()
