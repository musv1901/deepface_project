import math
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from image2base64.converters import base64_to_rgb


class WallView(object):

    def __init__(self):
        self._show_gui()

    def _show_gui(self):
        self.window = tk.Tk()
        self.window.title("Photo Wall")

        # Get the dimensions of the screen
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Set the size of the window to the maximum available size
        self.window.geometry("{}x{}".format(self.screen_width, self.screen_height))

    def refresh_img_wall(self, p_list):

        for child in self.window.winfo_children():
            for subchild in child.winfo_children():
                subchild.destroy()
            child.destroy()

        amount = len(p_list)
        count = 0

        # create a frame for each row
        for row in range(math.ceil(amount / 7)):
            row_frame = ttk.Frame(self.window, padding=10)
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
                text_label_age = ttk.Label(frame, text=str(p_list[count]["age"]), font=("Helvetica", 28))
                text_label_age.grid(row=1, column=0, sticky="nsew")

                text_label_gender = ttk.Label(frame, text=p_list[count]["gender"], font=("Helvetica", 28))
                text_label_gender.grid(row=2, column=0, sticky="nsew")

                text_label_emotion = ttk.Label(frame, text=p_list[count]["emotion"], font=("Helvetica", 28))
                text_label_emotion.grid(row=3, column=0, sticky="nsew")

                # load and display the image
                img = img = base64_to_rgb(p_list[count]["cropped_img"], "PIL")
                img = img.resize((240, 310))
                img_tk = ImageTk.PhotoImage(img)
                img_label.configure(image=img_tk)
                img_label.image = img_tk

                # update the count and load the next image
                count += 1
                if count == amount:
                    break

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()
