import json
import time
from deepface import DeepFace
import cv2
import uuid
import image2base64
import io
from io import BytesIO
import tkinter as tk
import customtkinter
from PIL import Image
from image2base64.converters import base64_to_rgb, rgb2base64


def getImage(frame):
    result = DeepFace.analyze(img_path=frame, enforce_detection=False, detector_backend='mtcnn')

    for face in result:
        txt = 'Gender: ' + face.get('dominant_gender') + '\n' \
              + 'Age: ' + str(face.get('age')) + '\n' \
              + 'ethnicity: ' + face.get('dominant_race') + '\n' \
              + 'Emotion: ' + face.get('dominant_emotion')

        print(txt)

        x = face.get('region')['x']
        y = face.get('region')['y']
        w = face.get('region')['w']
        h = face.get('region')['h']

        cropped_nd = frame[y:y + h, x:x + w]
        cropped_img = Image.fromarray(cropped_nd)

        isPresent(cropped_img)

        person = {
            "firstname": "",
            "lastname": "",
            "cropped_img_base": rgb2base64(cropped_img),
            "gender": face.get('dominant_gender'),
            "age": str(face.get('age')),
            "ethnicity": face.get('dominant_race'),
            "emotion": face.get('dominant_emotion')
        }

        with open("persons.json", "r") as file:
            data = json.load(file)

        data['persons'].append(person)

        with open("persons.json", "w") as file:
            json.dump(data, file)

        #cv2.rectangle(cropped_nd, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow('Cropped', cropped_nd)
        #cv2.putText(cropped_nd, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        # saveImage(frame)
    # cv2.imshow('Picture', frame)

    time.sleep(5)


def saveImage(frame):
    cv2.imwrite('Pictures\img' + str(uuid.uuid4()) + '.jpg', frame)


def isPresent(face):
    with open("persons.json", "r") as file:
        data = json.load(file)

    for element in data['persons']:
        img = base64_to_rgb(element.get('cropped_img_base'), "PIL")

        img.save("temp1.jpeg", "JPEG")
        face.save("temp2.jpeg", "JPEG")
        print(DeepFace.verify(img1_path="temp1.jpeg", img2_path="temp2.jpeg", detector_backend="mtcnn", enforce_detection=False))


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        getImage(frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
