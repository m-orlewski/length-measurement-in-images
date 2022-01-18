import os
import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, _tkinter_finder

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Length Measurement Project')
        self.window.geometry('1000x1000')


        self.button_load = tk.Button(self.window, text = "Wczytaj obraz", command = lambda: self.loadImage())
        self.button_load.place(x=10, y=10)


        n = tk.StringVar()
        self.choice = ttk.Combobox(self.window, textvariable=n)
        self.choice.grid(column = 1, row = 5)
        self.choice.pack()
        self.choice.pack_forget()

        self.window.mainloop()

    def loadImage(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title="Wybierz obraz",
                                            filetypes= (("JPG","*.jpg"), ("PNG","*.png"), ("JPEG","*.jpeg")))

        try:
            img = cv2.imread(filepath)
            frame2 = tk.Frame(self.window, bg="black", width=500, height=500)
            frame2.pack()
            label = tk.Label(frame2)
            label.grid(row=0, column=0)
            imgg = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=imgg)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            self.choice['values'] = ('1',
                                '2',
                                '3',
                                '4',
                                '5',
                                '6')
            self.choice.place(x=10, y=100)
            self.choice.pack()
        except IOError:
            print('Unable to open file!')


if __name__ == '__main__':
    app = App()