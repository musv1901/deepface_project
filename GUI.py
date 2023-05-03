import cv2
from PIL import Image, ImageTk
import time
import tkinter as tk

import main
from main import *


class GUI:

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = cv2.VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1

        self.update()

        self.window.mainloop()

    def update(self):
        frame = main.camera_feed(self.vid)

        if frame is not None:
            # display the frame on the canvas
            self.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
            self.canvas.image = frame

        # call the update method after the specified delay
        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
root = tk.Tk()
#root.geometry("500x500+50+50")
#root.attributes("-fullscreen", True)

GUI(root, "GUI-Test")

#
#     def showGUI(self):
#         root = tk.Tk()
#         root.geometry('1000x500')
#         root.title('Visitor Dashboard')
#
#         image_label = tk.Label(root)
#         image_label.pack()
#
#         description_label = tk.Label(root, font=("Arial", 14), wraplength=500)
#         description_label.pack()
#
# <<<<<<< HEAD
# # Define a function to display the next image and description
# =======
#         with open("persons_history.json", "r") as file:
#             data = json.load(file)
# >>>>>>> a0e24d493135084562554f2d64522da09c1af205
#
#         persons = data['persons']
#
# <<<<<<< HEAD
# current_image = 0
# def show_next_image():
#     global current_image
#     current_image += 1
#     if current_image >= len(persons):
# =======
#         # Define a function to display the next image and description
# >>>>>>> a0e24d493135084562554f2d64522da09c1af205
#         current_image = 0

# def show_next_image(current_image):
#     # current_image += 1
#     # if current_image >= len(persons):
#         current_image = 0
#     image = base64_to_rgb(persons[current_image]["cropped_img_base"])
#     image = image.resize((400, 400))
#     photo = ImageTk.PhotoImage(image)
#     image_label.configure(image=photo)
#     image_label.image = photo
#     description_label.configure(text=
#                                 str(persons[current_image]['gender']) + '\n'
#                                 + str(persons[current_image]['age']) + '\n'
#                                 + str(persons[current_image]['ethnicity']) + '\n'
#                                 # + str(persons[current_image]['emotion'])                  )
#
# # Create a button to display the next image
# next_button = tk.Button(root, text="Next", font=("Arial", 14), command=show_next_image(current_image))
# next_button.pack()

# root.mainloop()
