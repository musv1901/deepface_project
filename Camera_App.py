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
                box = model.detect_faces_opencv(frame)
                controller.update_view(box, i)
            view.window.update()

