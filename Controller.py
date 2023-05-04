import tkinter as tk
from PIL import Image

import cv2
from PIL import ImageTk


class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_view(self, frame, i):
        img = ImageTk.PhotoImage(frame.resize(
            (self.view.video_box_width, self.view.video_box_height), reducing_gap=1.0))

        if img is not None:
            # display the frame on the canvas
            self.view.canvases[i].create_image(0, 0, image=img, anchor=tk.NW)
            self.view.canvases[i].image = img

