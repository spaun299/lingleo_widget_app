import tkinter as tk
from lingleo_client import GetLeoDict
from utils import shelve_get, get_coordinates, create_text
from main_window import MainWindow
import config
import os
from PIL import Image, ImageTk


class Login(object):
    def __init__(self, root):
        root.state = 'main'
        self.root = root
        self.email = None
        self.password = None
        self.configure()
        self.write_canvas()

    def write_canvas(self):
        canvas = tk.Canvas(self.root)
        canvas.pack(expand=True, fill=tk.BOTH)
        self.write_background(canvas)
        create_text(canvas, 55, 30, 'Name')
        create_text(canvas, 50, 80, 'Password')
        create_text(canvas, 100, 5, 'Login to lingualeo')
        name_text = tk.StringVar(value="Name")
        password_text = tk.StringVar(value="Password")
        name = tk.Entry(canvas, textvariable=name_text, width=15,
                        font=self.root.font).grid(pady='30', padx='135', row=2)
        password = tk.Entry(canvas, textvariable=password_text, width=15,
                            font=self.root.font).grid(pady='0', padx='135', row=3)

    def write_background(self, canvas):
        background_image = Image.open(os.path.join(config.BACKGROUND_IMAGE_LOGIN))
        tkimage = ImageTk.PhotoImage(background_image)
        canvas.img = tkimage
        canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)

    def configure(self):
        coordinates = {'x': (self.root.winfo_screenwidth() / 2) - (config.WIDTH_SMALL_DEFAULT / 2),
                       'y': (self.root.winfo_screenheight() / 2) - (config.HEIGHT_SMALL_DEFAULT / 2),
                       'w': config.WIDTH_SMALL_DEFAULT, 'h': config.HEIGHT_SMALL_DEFAULT}
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))
        self.root.resizable(False, False)

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('main_coordinates')
        return coordinates
