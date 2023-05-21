import uuid

import requests

import json
import time
from confluent_kafka import Producer
import cv2
from PIL import Image, ImageTk
from image2base64.converters import base64_to_rgb, rgb2base64
import numpy as np


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

        # self.producer = Producer({'bootstrap.servers': '192.168.70.40:9092'})

        self.db = {
            "return_statistics": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com"
                                 "/ords/admin/operations/return_statistics",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

    def detect_faces_opencv(self, frame):
        start = time.time()
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

        print(time.time() - start)
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), face_count

    def to_analyze(self, video_feeds):
        screenshots = {"screens": []}

        for screen in video_feeds:
            base64 = rgb2base64(screen.read()[1], "JPEG")
            screenshots["screens"].append(base64)

        self.producer.produce(topic="toAnalyze", key=str(uuid.uuid4()), value=json.dumps(screenshots),
                              callback=delivery_report)
        self.producer.flush()

    def persons_statistics(self):
        response = requests.get(self.db.get("return_statistics"), self.db.get("headers"))

        return response.json()["items"]
