import tkinter as tk
import json
from PIL import ImageTk, Image
from image2base64.converters import base64_to_rgb, rgb2base64


class GUI:

    def showGUI(self):
        root = tk.Tk()
        root.geometry('1000x500')
        root.title('Visitor Dashboard')

        image_label = tk.Label(root)
        image_label.pack()

        description_label = tk.Label(root, font=("Arial", 14), wraplength=500)
        description_label.pack()

<<<<<<< HEAD
# Define a function to display the next image and description
=======
        with open("persons.json", "r") as file:
            data = json.load(file)
>>>>>>> a0e24d493135084562554f2d64522da09c1af205

        persons = data['persons']

<<<<<<< HEAD
current_image = 0
def show_next_image():
    global current_image
    current_image += 1
    if current_image >= len(persons):
=======
        # Define a function to display the next image and description
>>>>>>> a0e24d493135084562554f2d64522da09c1af205
        current_image = 0

    def show_next_image(current_image):
        current_image += 1
        if current_image >= len(persons):
            current_image = 0
        image = base64_to_rgb(persons[current_image]["cropped_img_base"])
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo
        description_label.configure(text=
                                    str(persons[current_image]['gender']) + '\n'
                                    + str(persons[current_image]['age']) + '\n'
                                    + str(persons[current_image]['ethnicity']) + '\n'
                                    + str(persons[current_image]['emotion'])
                                    )

    # Create a button to display the next image
    next_button = tk.Button(root, text="Next", font=("Arial", 14), command=show_next_image(current_image))
    next_button.pack()

    root.mainloop()
