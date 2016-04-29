import tkinter as tk
from lingleo_client import GetLeoDict
from utils import shelve_get, get_coordinates
from main_window import MainWindow


class Login(object):
    def __init__(self, root):
        root.state = 'main'
        self.root = root
        self.email = None
        self.password = None
        self.leo = GetLeoDict(self.email, self.password)
        self.write_canvas()

    def write_canvas(self):
        coordinates = get_coordinates('main', self.root)
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('main_coordinates')
        return coordinates
