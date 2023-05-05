import Model
import View
import Controller
import cv2

if __name__ == "__main__":
    model = Model.Model()
    view = View.View()
    controller = Controller.Controller(model, view)

    video_sources = [0, 0]
    video_feeds = []

    for source in video_sources:
        vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, view.screen_width / 2)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, view.screen_height / 2)
        vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        video_feeds.append(vid)

    while True:
        for i, feed in enumerate(video_feeds):
            ret, frame = feed.read()
            if ret:
                img = model.detect_faces(frame)
                controller.update_view(img, i)
        view.window.update()
