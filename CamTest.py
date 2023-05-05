import cv2
# Setting the video capture source to default (0)
cap = cv2.VideoCapture(0)
# Setting the resolution of the video capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# While loop to continuously capture frames from camera
while(True):
    # Read a frame from the camera
    ret, frame = cap.read()
    #frame = cv2.flip(frame, -1) # Flip camera vertically
    # Convert frame from BGR to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the original frame and grayscale frame
    cv2.imshow('OriginalBGR', frame)
    cv2.imshow('Grayscale', gray)
    
    # Wait for 30 milliseconds for a key event (extract sigfigs) and exit if 'ESC' or 'q' is pressed
    k = cv2.waitKey(30) & 0xff
    if key == 27: # ESCAPE key
        break
    elif key == 113 # q key
    break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
