import time

from deepface import DeepFace
import cv2
import uuid
from PIL import Image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def getImage():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        result = DeepFace.analyze(img_path=frame, enforce_detection=False)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            saveImage(frame)

        txt = 'Gender: ' + result.get('gender') + '\n' \
                  + 'Age: ' + str(result.get('age')) + '\n' \
                  + 'ethnicity: ' + result.get('dominant_race') + '\n' \
                  + 'Emotion: ' + result.get('dominant_emotion')

        cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow('Picture', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        time.sleep(10)
    cap.release()
    cv2.destroyAllWindows()

def saveImage(frame):
    cv2.imwrite('Pictures\img' + str(uuid.uuid4()) + '.jpg', frame)

getImage()
