import cv2
import os 
import numpy as np
from picamera2 import Picamera2

#Parameters
id = 0
font = cv2.FONT_HERSHEY_COMPLEX
height=1
boxColor=(0,0,255)      #BGR- GREEN
nameColor=(255,255,255) #BGR- WHITE
confColor=(255,255,0)   #BGR- TEAL

face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
# names related to id
names = ['None', 'Saumit', 'Bikram', 'Junaid']

# Create an instance of the PiCamera2 object
cam = Picamera2()
## Initialize and start realtime video capture
# Set the resolution of the camera preview
cam.preview_configuration.main.size = (640, 360)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate=30
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

while True:
    # Capture a frame from the camera
    frame=cam.capture_array()

    #Convert fram from BGR to grayscale
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Create a DS faces- array with 4 elements- x,y coordinates top-left corner), width and height
    faces = face_detector.detectMultiScale(
            frameGray,      # The grayscale frame to detect
            scaleFactor=1.1,# how much the image size is reduced at each image scale-10% reduction
            minNeighbors=5, # how many neighbors each candidate rectangle should have to retain it
            minSize=(150, 150)# Minimum possible object size. Objects smaller than this size are ignored.
            )
    for(x,y,w,h) in faces:
        namepos=(x+5,y-5) #shift right and up/outside the bounding box from top
        confpos=(x+5,y+h-5) #shift right and up/intside the bounding box from bottom
        #create a bounding box across the detected face
        cv2.rectangle(frame, (x,y), (x+w,y+h), boxColor, 3) #5 parameters - frame, topleftcoords,bottomrightcooords,boxcolor,thickness

        #recognizer.predict() method takes the ROI as input and
        #returns the predicted label (id) and confidence score for the given face region.
        id, confidence = recognizer.predict(frameGray[y:y+h,x:x+w])
        
        # If confidence is less than 100, it is considered a perfect match
        if confidence < 100:
            id = names[id]
            confidence = f"{100 - confidence:.0f}%"
        else:
            id = "unknown"
            confidence = f"{100 - confidence:.0f}%"

        #Display name and confidence of person who's face is recognized
        cv2.putText(frame, str(id), namepos, font, height, nameColor, 2)
        cv2.putText(frame, str(confidence), confpos, font, height, confColor, 1)

    # Display realtime capture output to the user
    cv2.imshow('Raspi Face Recognizer',frame)

    # Wait for 30 milliseconds for a key event (extract sigfigs) and exit if 'ESC' or 'q' is pressed
    key = cv2.waitKey(100) & 0xff
    #Checking keycode
    if key == 27:  # ESCAPE key
        break
    elif key == 113:  # q key
        break

# Release the camera and close all windows
print("\n [INFO] Exiting Program and cleaning up stuff")
cam.stop()
cv2.destroyAllWindows()
