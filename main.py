import time
from deepface import DeepFace
import cv2
import uuid


def getImage():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        result = DeepFace.analyze(img_path=frame, enforce_detection=False)

        for face in result:
            print(face)
            txt = 'Gender: ' + face.get('dominant_gender') + '\n' \
                  + 'Age: ' + str(face.get('age')) + '\n' \
                  + 'ethnicity: ' + face.get('dominant_race') + '\n' \
                  + 'Emotion: ' + face.get('dominant_emotion')

            print(txt)

            x = face.get('region')['x']
            y = face.get('region')['y']
            w = face.get('region')['w']
            h = face.get('region')['h']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            saveImage(frame)
        cv2.imshow('Picture', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        time.sleep(10)

    cap.release()
    cv2.destroyAllWindows()


def saveImage(frame):
    cv2.imwrite('Pictures\img' + str(uuid.uuid4()) + '.jpg', frame)


getImage()
