import cv2
import os
from picamera2 import Picamera2

#Parameters
count = 0
pos=(30,60) #top-left
font=cv2.FONT_HERSHEY_COMPLEX
height=1.5
color=(0,0,255) #BGR- RED
weight=3
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n----Enter User-id and press <return>----')
print("\n [INFO] Initializing face capture. Look the camera and wait!")

# Create an instance of the PiCamera2 object
cam = Picamera2()
## Set the resolution of the camera preview
cam.preview_configuration.main.size = (640, 360)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate=30
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

# Initialize individual sampling face count
while True:
    # Capture a frame from the camera
    frame=cam.capture_array()
    #Display count of images taken
    cv2.putText(frame,'Count:'+str(int(count)),pos,font,height,color,weight)

    #Convert fram from BGR to grayscale
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Create a DS faces- array with 4 elements- x,y coordinates top-left corner), width and height
    faces = face_detector.detectMultiScale(frameGray, 1.3, 5) # 3 parameters- frame,scale-factor,
    for (x,y,w,h) in faces:
        #create a bounding box across the detected face
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3) #tuple
        count += 1 # increment count
        # Save the captured bounded-grayscaleimage into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", frameGray[y:y+h,x:x+w]) #req os
    # Display the original frame to the user
    cv2.imshow('FaceCapture', frame)
    # Wait for 30 milliseconds for a key event (extract sigfigs) and exit if 'ESC' or 'q' is pressed
    key = cv2.waitKey(100) & 0xff
    #Checking keycode
    if key == 27:  # ESCAPE key
        break
    elif key == 113:  # q key
        break
    elif count >= 30: # Take 30 face sample and stop video capture
         break
# Release the camera and close all windows
print("\n [INFO] Exiting Program and cleaning up stuff")
cam.stop()
cv2.destroyAllWindows()
