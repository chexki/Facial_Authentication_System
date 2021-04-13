import numpy as np
import cv2
import os
import face_recognition
import itertools
from keras.models import load_model
from model import *

# Loading Liveness detection model
model = load_model('models\liveness.h5')
img_width, img_height = (96,96)

# Live not live

def liveness_predictions(file_name):
    file_name = 'static/uploads/' + file_name
    pred_image_n_live = load_img(file_name, target_size=(96, 96))
    imgArray = img_to_array(pred_image_n_live)
    imgArray = imgArray.reshape(1,img_width, img_height,3)
    imgArray = imgArray/float(255)
    outLabel = int(model.predict_classes(imgArray,verbose=0))
    # Real: 1    |  Fake: 0
    if outLabel == 1:
        return "Live"
    else:
        return "Not Live"


def evaluation_metric_main(input_,matches,threshold = 0.45):
    counter = itertools.count(0)
    [(next(counter), x) for x in list(input_) if x <= threshold]
    if np.mean(input_) <= threshold:
        print('1st Condition Satisfied')
        return "Matched"
    elif (matches.count(True) >= (len(matches) /2)): # (next(counter) >= (len(matches) /2)) &
        print('2nd Condition Satisfied')
        return "Matched"
    else:
        print('No Condition Satisfied')
        return "Unmatch"

def evaluation_metric(file_name,threshold = 0.45):
    path1 = 'static/captured/'
    files = os.listdir(path1)
    known_face_encodings = []
    known_face_names = 'Chetan' #[os.path.basename(path1)]

    for faces in files:
        try:
            face = face_recognition.load_image_file(path1 + faces)
            # print(face)
            face_encoding = face_recognition.face_encodings(face)[0]
            known_face_encodings.append(face_encoding)
        except:
            pass

    file_name = 'static/uploads/' + file_name
    unknown_image = face_recognition.load_image_file(file_name)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
    matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
    print(face_distances)
    print(matches)
    result = evaluation_metric_main(face_distances, matches, threshold=0.45)
    return result
