import tkinter as tk


class CameraView(object):

    def __init__(self):
        self.callbacks = {}
        self._show_gui()

    def _show_gui(self):
        self.window = tk.Tk()
        self.window.title("Video Feeds")

        self.canvases = []

        # Get the dimensions of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Set the size of the window to the maximum available size
        self.window.geometry("{}x{}".format(self.screen_width, self.screen_height))

        self.video_box_width = self.screen_width // 2
        self.video_box_height = self.screen_height // 2

        self.create_camera_feeds()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_camera_feeds(self):
        canvas1 = tk.Canvas(self.window, width=self.video_box_width, height=self.video_box_height)
        canvas1.pack(side="left", anchor="nw")
        self.canvases.append(canvas1)

        canvas2 = tk.Canvas(self.window, width=self.video_box_width, height=self.video_box_height)
        canvas2.pack(side="right", anchor="nw")
        self.canvases.append(canvas2)

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()
