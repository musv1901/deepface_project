import time
from Camera_View import CameraView
from Camera_Controller import CameraController
from Camera_Model import CameraModel
import cv2


if __name__ == "__main__":
    model = CameraModel()
    view = CameraView()
    controller = CameraController(model=model, view=view)

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
                model.to_analyze(video_feeds=video_feeds)
                start = time.time()
            ret, frame = feed.read()
            if ret:
                controller.update_view(frame, i)
            view.window.update()
