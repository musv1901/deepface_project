import csv
import uuid
from datetime import datetime
import requests
import json
import time
from confluent_kafka import Producer
import cv2
from PIL import Image, ImageTk
from image2base64.converters import base64_to_rgb, rgb2base64
import numpy as np
import pandas as pd


def delivery_report(errmsg, msg):
    if errmsg is not None:
        print("Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
        return
    print('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


class CameraModel:

    def __init__(self):
        protoFile = "Models/deploy.prototxt.txt"
        modelFile = "Models/res10_300x300_ssd_iter_140000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(protoFile, modelFile)

        self.producer = Producer({'bootstrap.servers': '192.168.70.40:9092'})

        self.db = {
            "return_statistics": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com"
                                 "/ords/admin/operations/return_statistics",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

        self.stats_csv = "data/stats.csv"

    def detect_faces_opencv(self, frame):
        face_count = 0
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
                face_count += 1

        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), face_count

    def to_analyze(self, video_feeds):
        screenshots = {"screens": []}

        for screen in video_feeds:
            base64 = rgb2base64(screen.read()[1], "JPEG")
            screenshots["screens"].append(base64)

        self.producer.produce(topic="toAnalyze", key=str(uuid.uuid4()), value=json.dumps(screenshots),
                              callback=delivery_report)
        self.producer.flush()

    def update_stats_csv(self):
        response = requests.get(self.db.get("return_statistics"), self.db.get("headers"))

        for e in response.json()["items"]:
            timestamp = datetime.fromtimestamp(time.time(), tz=None)
            data = [timestamp, e["male_ratio"], e["women_ratio"], e["age_avg"],
                    e["total_count"], e["angry_count"], e["fear_count"], e["neutral_count"],
                    e["sad_count"], e["disgust_count"], e["happy_count"], e["surprise_count"]]

            with open(self.stats_csv, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

    def get_stats(self):
        return pd.read_csv(self.stats_csv)
