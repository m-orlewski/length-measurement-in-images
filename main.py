from tkinter import *
from tkinter import filedialog

def browseFiles():
    

    

    


window = Tk()
window.title('')

window.geometry('500x500')
window.config(background = "white")

button_explore = Button(window,
                        text = "Wczytaj zdjęcie",
                        command = browseFiles)
  
button_exit = Button(window,
                     text = "Zakończ",
                     command = exit)

button_explore.grid(column = 1, row = 2)
button_exit.grid(column = 1,row = 3)

window.mainloop()