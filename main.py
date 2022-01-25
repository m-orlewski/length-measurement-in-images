import os
import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from utils import *

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Pomiary długości na obrazie')
        self.window.geometry('1280x720')

        self.button_load = tk.Button(self.window, text = 'Wczytaj obraz', command = lambda: self.loadImage())
        self.button_load.place(x=10, y=10)

        self.labelWidth = tk.StringVar()
        self.labelWidth.set('Podaj szerokość obiektu referencyjnego(cm):')
        self.label2 = tk.Label(self.window, textvariable=self.labelWidth)
        self.label2.place(x=10, y=50)
        self.widthEntry = tk.Entry(self.window)
        self.widthEntry.place(x=10, y=80)

        self.labelChoice = tk.StringVar()
        self.labelChoice.set('Wybierz obiekt referencyjny:')
        self.label3 = tk.Label(self.window, textvariable=self.labelChoice)
        self.label3.place(x=10, y=110)
        self.n = tk.StringVar()
        self.choice = ttk.Combobox(self.window, textvariable=self.n)
        self.choice.place(x=10, y=140)

        self.measure_button = tk.Button(self.window, text = 'Pomiar długości', command = lambda: self.measureLengths())
        self.measure_button.pack()
        self.measure_button.pack_forget()

        self.label = tk.Label(self.window, pady=20)
        self.label.pack(pady=(10, 0))


        self.window.mainloop()

    def loadImage(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='Wybierz obraz',
                                            filetypes= (('JPG','*.jpg'), ('PNG','*.png'), ('JPEG','*.jpeg')))

        try:
            self.img = cv2.imread(filepath)
            self.labeled_image, count, self.edges = labelObjects(self.img)

            self.choice['values'] = tuple([str(i+1) for i in range(count)])
            self.choice.current(0)
            self.measure_button.pack()
            self.measure_button.place(x=10, y=200)

            self.displayImage(self.img)
            
        except IOError:
            print('Unable to open file!')

    def measureLengths(self):
        choice = self.n.get()
        width = float(self.widthEntry.get())
        measured_image = measureObjects(self.edges, choice, width, self.img.copy())
        self.displayImage(measured_image)

    def displayImage(self, img):
        w = 0
        h = 0
        if img.shape[0] > img.shape[1]:
            h = int(500 * img.shape[0] / img.shape[1])
            img = cv2.resize(img, (500, h))
        else:
            w = int(700 * img.shape[1] / img.shape[0])
            img = cv2.resize(img, (w, 700))
        
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(img)
        self.label.imgtk = img
        if w:
            self.label.configure(image=img, width=w, height=700)
        else:
            self.label.configure(image=img, width=500, height=h)

if __name__ == '__main__':
    app = App()