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
import multiprocessing as mp


def cameraFeed(cap):
    while True:
        ret, frame = cap.read()

        detectedFaces = DeepFace.detectFace(img_path=frame, enforce_detection=False, detector_backend='mtcnn')
        cv2.imshow('camera-feed', frame)

        for face in detectedFaces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x + w, y + h), (0, 255, 0), 2)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def analyzeScreenshot(cap):
    while True:
        ret, frame = cap.read()

        result = DeepFace.analyze(img_path=frame, enforce_detection=False, detector_backend='mtcnn')

        p_list = {
            "persons": [

            ]
        }

        for face in result:
            cropped = getcroppedFace(face)
            info = getpersonInfo(face, cropped)
            p_list["persons"].append(info)

            if not isPresent(cropped):
                storefaceHistory(info)

        with open("persons_present.json", "w") as file:
            json.dump(p_list, file)

        time.sleep(15)

def getpersonInfo(face_dict, cropped_face):

    return {
        "firstname": "",
        "lastname": "",
        "cropped_img_base": rgb2base64(cropped_face),
        "gender": face_dict.get('dominant_gender'),
        "age": str(face_dict.get('age')),
        "ethnicity": face_dict.get('dominant_race'),
        "emotion": face_dict.get('dominant_emotion')
    }

def buildpresentPersons(faces_list):


def storefaceHistory(face_info):


    with open("persons_history.json", "r") as file:
        data = json.load(file)

    data['persons'].append(face_info)

    with open("persons_history.json", "w") as file:
        json.dump(data, file)


def getcroppedFace(face_dict):
    x = face_dict.get('region')['x']
    y = face_dict.get('region')['y']
    w = face_dict.get('region')['w']
    h = face_dict.get('region')['h']

    cropped_nd = face_dict[y:y + h, x:x + w]
    return Image.fromarray(cropped_nd)


def isPresent(cropped_face):
    with open("persons_history.json", "r") as file:
        data = json.load(file)

        for element in data['persons']:

            img = base64_to_rgb(element.get('cropped_img_base'), "PIL")

            img.save("temp1.jpeg", "JPEG")
            cropped_face.save("temp2.jpeg", "JPEG")
            dict = DeepFace.verify(img1_path="temp1.jpeg", img2_path="temp2.jpeg", detector_backend="mtcnn",
                                   enforce_detection=False)

            if dict['verified']:
                return True

        return False


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    p1 = mp.Process(target=cameraFeed(cap))
    p2 = mp.Process(target=analyzeScreenshot(cap))


