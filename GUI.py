import tkinter as tk
import customtkinter

root = tk.Tk()

root.geometry('1000x500')
root.title('Visitor Dashboard')

label = tk.Label(root, text='Hello Visitor!', font=('Arial', 18))
label.pack(padx=20, pady=20)



root.mainloop()

