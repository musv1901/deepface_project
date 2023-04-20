import tkinter as tk
import json
from PIL import ImageTk, Image


class GUI:

    def showGUI(self):
        root = tk.Tk()
        root.geometry('1000x500')
        root.title('Visitor Dashboard')

        image_label = tk.Label(root)
        image_label.pack()

        description_label = tk.Label(root, font=("Arial", 14), wraplength=500)
        description_label.pack()

        with open("persons.json", "r") as file:
            data = json.load(file)

        persons = data['persons']

        # Define a function to display the next image and description
        current_image = 0

    def show_next_image(current_image):
        current_image += 1
        if current_image >= len(persons):
            current_image = 0
        image = Image.frombytes(data=persons[current_image]["cropped_img_base"], decoder_name='base64')
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
