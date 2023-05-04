import Model
import View
import Controller
import cv2
import concurrent.futures

if __name__ == "__main__":
    model = Model.Model()
    view = View.View()
    controller = Controller.Controller(model, view)

    video_sources = [0, 0]
    video_feeds = []

    for source in video_sources:
        vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        video_feeds.append(vid)


def process_video_feed(video_feed, index):
    while True:
        ret, frame = video_feed.read()

        img = model.detect_faces(frame)
        controller.update_view(img, index)


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_video_feed, video_feeds[i], i) for i in range(len(video_feeds))]

    view.window.mainloop()

    for future in futures:
        future.cancel()
