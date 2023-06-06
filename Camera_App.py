import time
from Camera_View import CameraView
from Camera_Model import CameraModel
import cv2
import pandas as pd


def update_plots():
    df = model.get_stats()
    df['time'] = pd.to_datetime(df['time'])
    latest_data = df.iloc[-1]
    history_data = df.tail(10)

    view.update_gender_plot([latest_data["male_ratio"], latest_data["women_ratio"]])
    view.update_age_plot([history_data["time"], history_data["age_avg"]])


if __name__ == "__main__":
    view = CameraView()
    model = CameraModel()

    video_sources = [0, 0]
    video_feeds = []

    TIME_TO_SCREENSHOT = 10

    for source in video_sources:
        vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, view.screen_width / 2)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, view.screen_height / 2)
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        video_feeds.append(vid)

    view.window.update()
    start = time.time()
    while True:
        face_count_sum = 0
        for i, feed in enumerate(video_feeds):
            if int(time.time() - start) > TIME_TO_SCREENSHOT:
                # model.to_analyze(video_feeds=video_feeds)
                #model.update_stats_csv()
                #update_plots()
                start = time.time()
            ret, frame = feed.read()
            if ret:
                img, face_count = model.detect_faces_opencv(frame)
                view.update_feeds(img, i)
                #face_count_sum += face_count
            view.window.update()
