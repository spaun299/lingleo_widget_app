import tkinter as tk
from lingleo_client import GetLeoDict
from utils import shelve_get, get_coordinates
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
        background_image = Image.open(os.path.join('static/images/background_login.jpg'))
        tkimage = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=tkimage)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

        cwgt = tk.Canvas(self.root)
        cwgt.pack(expand=True, fill=tk.BOTH)
        # keep a link to the image to stop the image being garbage collected
        cwgt.img = tkimage
        cwgt.create_image(0, 0, anchor=tk.NW, image=tkimage)

    def configure(self):
        coordinates = {'x': (self.root.winfo_screenwidth() / 2) - (config.WIDTH_SMALL_DEFAULT / 2),
                       'y': (self.root.winfo_screenheight() / 2) - (config.HEIGHT_SMALL_DEFAULT / 2),
                       'w': config.WIDTH_SMALL_DEFAULT, 'h': config.HEIGHT_SMALL_DEFAULT}
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('main_coordinates')
        return coordinates
