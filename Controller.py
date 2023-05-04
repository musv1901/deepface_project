from GUI import GUI
import cv2


class Controller:

    def __init__(self):
        self.video_sources = [0, 0]
        self.video_feeds = []

    def start(self):

        for source in self.video_sources:
            vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
            vid.set(cv2.CAP_PROP_FRAME_WIDTH, gui.screen_width / 2)
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, gui.screen_height / 2)
            vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            self.video_feeds.append(vid)

        while True:
            for i, feed in enumerate(self.video_feeds):
                ret, frame = feed.read()
                if ret:
                    gui.update(frame, i)


controller = Controller()
gui = GUI(controller)
