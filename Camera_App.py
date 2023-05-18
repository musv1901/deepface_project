import json
import time
from Camera_View import CameraView
from Camera_Controller import CameraController
from Camera_Model import CameraModel
import cv2
from image2base64.converters import rgb2base64, base64_to_rgb
from confluent_kafka import Producer
import uuid


def to_analyze():
    screenshots = {"screens": []}

    for screen in video_feeds:
        base64 = rgb2base64(screen.read()[1], "JPEG")
        screenshots["screens"].append(base64)

    producer.produce(topic="toAnalyze", key=str(uuid.uuid4()), value=json.dumps(screenshots), callback=delivery_report)
    producer.flush()


def delivery_report(errmsg, msg):
    if errmsg is not None:
        print("Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
        return
    print('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


if __name__ == "__main__":
    model = CameraModel()
    view = CameraView()
    controller = CameraController(model=model, view=view)

    producer = Producer({'bootstrap.servers': '192.168.70.40:9092'})

    video_sources = [0, 0]
    video_feeds = []

    TIME_TO_SCREENSHOT = 30

    for source in video_sources:
        vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, view.screen_width / 2)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, view.screen_height / 2)
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        video_feeds.append(vid)

    start = time.time()
    while True:
        for i, feed in enumerate(video_feeds):
            if int(time.time() - start) > TIME_TO_SCREENSHOT:
                to_analyze()
                start = time.time()
            ret, frame = feed.read()
            if ret:
                box = model.detect_faces_opencv(frame)
                controller.update_view(box, i)
            view.window.update()
