import math
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from image2base64.converters import base64_to_rgb
from functools import partial


class WallView(object):

    def __init__(self, model):
        self.model = model
        self.image_width = 240
        self.image_padding = 10
        self.start_time = time.time()

        self.refresh_stop = False
        self._show_gui()

    def _show_gui(self):
        self.window = tk.Tk()
        self.window.bind("<Button-1>", self.set_focus)
        self.window.title("Photo Wall")

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry("{}x{}".format(self.screen_width, self.screen_height))

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        image_wall_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=image_wall_frame, anchor="nw")

        scrollbar.config(command=self.canvas.yview)
        self.image_wall_frame = image_wall_frame

    def refresh_img_wall(self, p_list):

        # destroy all subchild frames (for rebuilding)
        for child in self.image_wall_frame.winfo_children():
            child.destroy()

        amount = len(p_list)
        count = 0

        num_images_per_row = self.screen_width // (self.image_width + self.image_padding)

        for row, i in enumerate(range(math.ceil(amount / num_images_per_row))):

            # configure row frame
            row_frame = ttk.Frame(self.image_wall_frame, padding=self.image_padding)
            row_frame.grid(row=row, column=0, sticky="ew")

            for col in range(num_images_per_row):
                # configure column frame
                frame = ttk.Frame(row_frame, padding=self.image_padding)
                style = ttk.Style()
                style.configure("MyFrame.TFrame", borderwidth=3, relief="solid")
                frame.configure(style="MyFrame.TFrame")
                frame.grid(row=0, column=col, sticky="nsew")
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)

                # configure entry (for insert name)
                entry_name = ttk.Entry(frame, font=("Segoe UI", 16))
                if not p_list[count]["name"]:
                    entry_name.insert(0, "Enter a name")
                else:
                    entry_name.insert(0, p_list[count]["name"])
                    entry_name.config(state="disabled")
                entry_name.bind("<FocusIn>", self.on_entry_focus_in)
                entry_name.bind("<FocusOut>",
                                lambda event, entry=entry_name, person=p_list[count]: self.on_entry_focus_out(entry,
                                                                                                              person))
                entry_name.grid(row=1, column=0, sticky="nsew")

                # configure text labels (age, gender, emotion)
                text_label_age = ttk.Label(frame, text="Age: " + str(p_list[count]["age"]), font=("Segoe UI", 16))
                text_label_age.grid(row=2, column=0, sticky="nsew")

                text_label_gender = ttk.Label(frame, text='Gender: ' + p_list[count]["gender"], font=("Segoe UI", 16))
                text_label_gender.grid(row=3, column=0, sticky="nsew")

                text_label_emotion = ttk.Label(frame, text='Emotion: ' + p_list[count]["emotion"], font=("Segoe UI", 16))
                text_label_emotion.grid(row=4, column=0, sticky="nsew")

                # configure img frame
                img = base64_to_rgb(p_list[count]["cropped_img"], "PIL")
                img_tk = ImageTk.PhotoImage(img)
                img_label = ttk.Label(frame)
                img_label.bind("<Button-1>",
                               lambda event, person=p_list[count]: self.on_img_click(person))
                img_label.grid(row=0, column=0, sticky="nsew")
                img_label.configure(image=img_tk)
                img_label.image = img_tk

                count += 1
                if count == amount:
                    break

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), "units")

    def on_entry_focus_in(self, event):
        self.refresh_stop = True
        if event.widget.get() == "Enter a name":
            event.widget.delete(0, "end")

    def on_entry_focus_out(self, entry, person):
        if str(entry.cget("state")) != "disabled":
            if entry.get() == "":
                entry.insert(0, "Enter a name")
            else:
                p_id = person["id"]
                p_name = entry.get()
                entry.config(state="disabled")
                self.model.insert_name_db(p_id, p_name)
                self.start_time = time.time()

        self.refresh_stop = False

    def on_img_click(self, person):
        popup_window = tk.Toplevel()
        # popup_window.

    def set_focus(self, event):
        event.widget.focus_set()

    def run(self):
        self.window.mainloop()

    def on_close(self):
        self.window.destroy()
