import json
import time
from deepface import DeepFace
import cv2
from PIL import Image, ImageTk
from image2base64.converters import base64_to_rgb, rgb2base64
import csv
from datetime import datetime
import numpy as np


class CameraModel:

    def __init__(self):
        protoFile = "Models/deploy.prototxt.txt"
        modelFile = "Models/res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(protoFile, modelFile)

    def detect_faces_opencv(self, frame):
        start = time.time()
        (h, w) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # print(str(time.time() - start))
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def get_cropped_face(face_dict, frame):
        x = face_dict.get('region')['x']
        y = face_dict.get('region')['y']
        w = face_dict.get('region')['w']
        h = face_dict.get('region')['h']

        cropped_nd = frame[y:y + h, x:x + w]
        return Image.fromarray(cropped_nd)

    def is_present(cropped_face):
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

    def get_persons_statistics():
        sum_age = 0
        male_count = 0

        with open("persons_present.json", "r") as file:
            data = json.load(file)

        for element in data['persons']:
            sum_age = sum_age + float(element.get("age"))

            if element.get("gender") == "Man":
                male_count = male_count + 1

        avg_age = sum_age / len(data['persons'])
        male_percentage = float(male_count / len(data['persons'])) * 100
        woman_percentage = 100 - male_percentage

        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        str_date_time = date_time.strftime("%d-%m-%Y %H:%M:%S")

        pers_stats = {
            "timestamp": str_date_time,
            "avg_age": avg_age,
            "male_percentage": male_percentage,
            "woman_percentage": woman_percentage
        }

        # create_timestamp(pers_stats)

        return pers_stats

    def create_timestamp(pers_stats):
        field_names = ['timestamp', 'avg_age', 'male_percentage', 'woman_percentage']

        with open('stats_history.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writerow(pers_stats)
