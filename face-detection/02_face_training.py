import cv2
import numpy as np
from PIL import Image
import os

path = 'dataset'
# Using LBPH(Local Binary Patterns Histograms) recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml"); #create an instance
# function to read the images in the dataset, convert them to grayscale values, return samples
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
#returns two arrays faces and ids
faces,ids = getImagesAndLabels(path)
#Train the LBPH recognizer using the face samples and their corresponding labels
recognizer.train(faces, np.array(ids))
# if trainer folder doesnt exist create:
if not os.path.exists("trainer"):
    os.makedirs("trainer")
#save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') 
# Print the numer of faces trained and then exit the program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
