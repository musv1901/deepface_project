import json
import time
from deepface import DeepFace
import cv2
from PIL import Image, ImageTk
from image2base64.converters import base64_to_rgb, rgb2base64
from confluent_kafka import Producer, Consumer
import csv
from datetime import datetime
import torch
import numpy as np


class Model:

    def __init__(self):
        self.yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.yolo_model = self.yolo_model.to(self.device)


    def detect_faces(self, frame):
        start = time.time()

        detectedFaces = DeepFace.extract_faces(img_path=frame, enforce_detection=False, detector_backend='opencv',
                                               align=False)
        for face in detectedFaces:
            if face['confidence'] > 9:
                x = face['facial_area']['x']
                y = face['facial_area']['y']
                w = face['facial_area']['w']
                h = face['facial_area']['h']

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        print(time.time() - start)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def detect_faces_mediapipe(self, frame):



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



