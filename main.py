import os
import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, _tkinter_finder
from utils import *

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Pomiary długości na obrazie')
        self.window.geometry('1000x1000')


        self.button_load = tk.Button(self.window, text = 'Wczytaj obraz', command = lambda: self.loadImage())
        self.button_load.place(x=10, y=10)


        self.label_choice = tk.StringVar()
        self.choice = ttk.Combobox(self.window, textvariable=self.label_choice)
        self.choice.grid(column = 1, row = 5)
        self.choice.pack()
        self.choice.pack_forget()

        self.measure_button = tk.Button(self.window, text = 'Pomiar długości', command = lambda: self.measureLengths())
        self.measure_button.pack()
        self.measure_button.pack_forget()

        self.window.mainloop()

    def loadImage(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Wybierz obraz',
                                            filetypes= (('JPG','*.jpg'), ('PNG','*.png'), ('JPEG','*.jpeg')))

        try:
            img = cv2.imread(filepath)
            labeled_image = labelObjects(img)

            self.choice['values'] = ('1',
                                '2',
                                '3',
                                '4',
                                '5',
                                '6')
            self.choice.current(0)
            self.choice.pack()
            self.choice.place(x=10, y=100)
            self.measure_button.pack()
            self.measure_button.place(x=10, y=200)
        except IOError:
            print('Unable to open file!')

    def measureLengths(self):
        choice =self.label_choice.get()
        measured_image = measureObjects(choice)


if __name__ == '__main__':
    app = App()