#import libraries
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as numpy

faceclassi = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
classifier = load_model('./Emotion_Detection.h5')

class_names = ['Angry','Happy','Sad','Surprise','Neutral']
capture = cv2.VideoCapture(0)

while True:
    #capture single frame from video
    ret, frame = capture.read()
    names = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceclassi.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48,48), interpolation=cv2.INTER_AREA)


        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.extend_dims(roi,axis=0)

    #make a prediction on the ROI,then lookup the class

            predict = classifier.predict(roi)[0]
            print("\nprediction = ",predict)
            label = class_names[predict.argmax()]
            print("\nprediction max = ",predict.argmax())
            print("\nlabel = ",label)
            label_pos = (x,y)
            cv2.putText(frame, label, label_pos, cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        else:
            cv2.putText(frame, 'NO Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)

        print("\n\n")
        

    #to stop the script
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()


