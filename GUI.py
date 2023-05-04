import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import main
import cv2


class GUI:

    def __init__(self, window, window_title, video_sources):
        self.window = window
        self.window.title(window_title)

        self.video_sources = video_sources
        self.captures = []
        self.canvases = []

        # Create a Notebook widget
        self.notebook = ttk.Notebook(window)
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

        self.create_live_stats()
        self.create_camera_feeds()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1

        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def create_camera_feeds(self):
        # Create GUI elements --- camera feeds
        for i, source in enumerate(self.video_sources):
            vid = cv2.VideoCapture(source, cv2.CAP_DSHOW)
            vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_box_width)
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_box_height)
            vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

            if vid.isOpened():
                self.captures.append(vid)
                canvas = tk.Canvas(self.tab1, width=self.video_box_width, height=self.video_box_height)

                if i == 0:
                    canvas.pack(side="left", anchor="nw")
                elif i == 1:
                    canvas.pack(side="right", anchor="ne")

                self.canvases.append(canvas)
            else:
                print(f"Warning: Could not open video source {i}")

    def create_live_stats(self):

        label_frame = tk.Frame(self.tab1)
        label_frame.place(relx=0.5, rely=0.9, anchor="center")
        label = tk.Label(label_frame, text="TEST123", font=("Arial", 40))
        label.pack()

    def update(self):
        for i, vid in enumerate(self.captures):
            ret, frame = vid.read()
            if ret:
                #img = ImageTk.PhotoImage(
                    #main.detect_faces(frame).resize((self.video_box_width, self.video_box_height), reducing_gap=1.0))

                img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((self.video_box_width, self.video_box_height), reducing_gap=1.0))

                if img is not None:
                    # display the frame on the canvas
                    self.canvases[i].create_image(0, 0, image=img, anchor=tk.NW)
                    self.canvases[i].image = img

        # call the update method after the specified delay
        self.window.after(self.delay, self.update)

    def on_close(self):
        # Release all video captures when the GUI window is closed
        for vid in self.captures:
            vid.release()
        self.window.destroy()


# Create a window and pass it to the Application object
root = tk.Tk()
gui = GUI(root, "GUI-Test", [0, 0])

# root.geometry("500x500+50+50")
# root.attributes("-fullscreen", True)


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


# root.geometry("500x500+50+50")
# root.attributes("-fullscreen", True)


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
