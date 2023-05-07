import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class View(object):

    def __init__(self):
        self.callbacks = {}
        self._show_gui()

    def _show_gui(self):
        self.window = tk.Tk()
        self.window.title("GUI")

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

        self.create_camera_feeds()
        self.create_img_wall()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_camera_feeds(self):
        canvas1 = tk.Canvas(self.tab1, width=self.video_box_width, height=self.video_box_height)
        canvas1.pack(side="left", anchor="nw")
        self.canvases.append(canvas1)

        canvas2 = tk.Canvas(self.tab1, width=self.video_box_width, height=self.video_box_height)
        canvas2.pack(side="right", anchor="nw")
        self.canvases.append(canvas2)

    def create_img_wall(self):

        img = Image.open(r"Pictures/480_620_cropped/b1c0bc5b-03c0-4fa7-b93e-b1bebd123b8bupscale_resize_.jpeg")
        img1 = img.resize((240, 310))

        for row in range(3):
            for col in range(5):
                frame = ttk.Frame(self.tab2, width=240, height=310)
                frame.grid(row=row, column=col)
                label = ttk.Label(frame)
                label.pack()

                image = ImageTk.PhotoImage(img1)
                label.configure(image=image)
                label.image = image

    def bind_commands(self):
        self.btn.config(command=self.callbacks['import'])

    def add_callback(self, key, method):
        self.callbacks[key] = method

    def run(self):
        self.window.mainloop()

    def on_close(self):

        self.window.destroy()
