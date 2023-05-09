import cv2
import os
import numpy as np

# Using LBPH(Local Binary Patterns Histograms) recognizer
recognizer=cv2.face.LBPHFaceRecognizer_create()
face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path='dataset'

# function to read the images in the dataset, convert them to grayscale values, return samples
def getImagesAndLabels(path):
    faceSamples=[]
    ids = []

    for file_name in os.listdir(path):
        if file_name.endswith(".jpg"):
            id = int(file_name.split(".")[1])
            img_path = os.path.join(path, file_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces = face_detector.detectMultiScale(img)

            for (x, y, w, h) in faces:
                faceSamples.append(img[y:y+h, x:x+w])
                ids.append(id)

    return faceSamples, ids


def trainRecognizer(faces, ids):
    recognizer.train(faces, np.array(ids))
    # Create the 'trainer' folder if it doesn't exist
    if not os.path.exists("trainer"):
        os.makedirs("trainer")
    # Save the model into 'trainer/trainer.yml'
    recognizer.write('trainer/trainer.yml')


print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
# Get face samples and their corresponding labels
faces, ids = getImagesAndLabels(path)

#Train the LBPH recognizer using the face samples and their corresponding labels
trainRecognizer(faces, ids)


# Print the number of unique faces trained
num_faces_trained = len(set(ids))
print("\n [INFO] {} faces trained. Exiting Program".format(num_faces_trained))
