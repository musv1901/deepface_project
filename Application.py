import time
import Model
import View
import Controller
import cv2
from multiprocessing import Process, Queue
import uuid


def process_frames(q):
    while True:
        data = q.get()

        cv2.imwrite("Pictures/raw" + str(uuid.uuid4()) + ".jpeg", data)


if __name__ == "__main__":
    model = Model.Model()
    view = View.View()
    controller = Controller.Controller(model, view)

    video_sources = [0, 0]
    video_feeds = []

    TIME_TO_SCREENSHOT_SECS = 30

    p_queue = Queue()
    p_process = Process(target=process_frames, args=(p_queue,))
    p_process.start()

    for source in video_sources:
        vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, view.screen_width / 2)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, view.screen_height / 2)
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        video_feeds.append(vid)

    start = time.time()
    while True:
        for i, feed in enumerate(video_feeds):
            ret, frame = feed.read()
            if ret:
                if time.time() - start > TIME_TO_SCREENSHOT_SECS:
                    p_queue.put(frame)
                    start = time.time()
                box = model.detect_faces(frame)
                controller.update_view(box, i)
            view.window.update()
