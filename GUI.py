import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import multiprocessing as mp
import cv2


class GUI:

    def __init__(self, controller):

        self.window = tk.Tk()
        self.window.title("GUI")

        self.video_sources = None
        self.captures = []
        self.canvases = []

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        # Create a separate Frame for each tab
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        # Add the tabs to the Notebook
        self.notebook.add(self.tab1, text="Live Feed")
        self.notebook.add(self.tab2, text="Wall")

        # Get the dimensions of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Set the size of the window to the maximum available size
        self.window.geometry("{}x{}".format(self.screen_width, self.screen_height))

        self.video_box_width = self.screen_width // 2

        self.video_box_height = self.screen_height // 2

        self.controller = controller

        self.create_camera_feeds()
        self.create_start_btn()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def get_window(self):
        return self.window

    def create_camera_feeds(self):

        canvas1 = tk.Canvas(self.tab1, width=self.video_box_width / 2, height=self.video_box_height / 2)
        canvas1.pack(side="left", anchor="nw")
        self.canvases.append(canvas1)

        canvas2 = tk.Canvas(self.tab1, width=self.video_box_width / 2, height=self.video_box_height / 2)
        canvas2.pack(side="right", anchor="nw")
        self.canvases.append(canvas2)

    def create_start_btn(self):

        btn = tk.Button(self.tab1, text="Start", command=self.controller.start())
        btn.pack()

    def start_multiprocessing(self):

        processes = [mp.Process(target=self.update, args=(i,)) for i in range(len(self.video_sources))]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

    def update(self, frame, i):

        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize(
            (self.video_box_width, self.video_box_height), reducing_gap=1.0))

        if img is not None:
            # display the frame on the canvas
            self.canvases[i].create_image(0, 0, image=img, anchor=tk.NW)
            self.canvases[i].image = img

    def on_close(self):
        # Release all video captures when the GUI window is closed
        for vid in self.captures:
            vid.release()
        self.window.destroy()
