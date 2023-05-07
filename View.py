import math
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os


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

        path = r"Pictures/480_620_cropped"

        # img = Image.open(r"Pictures/480_620_cropped/b1c0bc5b-03c0-4fa7-b93e-b1bebd123b8bupscale_resize_.jpeg")
        # img1 = img.resize((120 * 2, 155 * 2))

        folder = os.listdir(path)
        amount = len(folder)
        count = 0

        # create a frame for each row
        for row in range(math.ceil(amount / 7)):
            row_frame = ttk.Frame(self.tab2, padding=10)
            row_frame.grid(row=row, column=0, sticky="ew")
            row_frame.columnconfigure(0, weight=1)

            # create frames for each image and text
            for col in range(7):
                frame = ttk.Frame(row_frame, padding=10)
                # Create a ttk.Style object
                style = ttk.Style()

                # Set the style properties for the Frame widget
                style.configure("MyFrame.TFrame", borderwidth=3, relief="solid")

                # Apply the style to the Frame widget
                frame.configure(style="MyFrame.TFrame")

                frame.grid(row=0, column=col, sticky="nsew")
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)

                # create labels for the image and text
                img_label = ttk.Label(frame)
                img_label.grid(row=0, column=0, sticky="nsew")
                text_label_age = ttk.Label(frame, text="AGE", width=20)
                text_label_age.grid(row=1, column=0, sticky="nsew")

                text_label_gender = ttk.Label(frame, text="GENDER", width=20)
                text_label_gender.grid(row=2, column=0, sticky="nsew")

                text_label_emotion = ttk.Label(frame, text="EMOTION", width=20)
                text_label_emotion.grid(row=3, column=0, sticky="nsew")

                # load and display the image
                img = Image.open(os.path.join(path, folder[count]))
                img = img.resize((240, 310))
                img_tk = ImageTk.PhotoImage(img)
                img_label.configure(image=img_tk)
                img_label.image = img_tk

                # update the count and load the next image
                count += 1
                if count == amount:
                    break

    def bind_commands(self):
        self.btn.config(command=self.callbacks['import'])

    def add_callback(self, key, method):
        self.callbacks[key] = method

    def run(self):
        self.window.mainloop()

    def on_close(self):

        self.window.destroy()
