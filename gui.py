from tkinter import *
from tkinter import ttk
root = Tk()

myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="Test123")
myButton = Button(root, text="touch me!",padx=50)

myLabel1.grid(row=0, column=3)
myLabel2.grid(row=1, column=0)
myButton.grid(row=1, column=1)

root.mainloop()