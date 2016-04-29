import tkinter as tk
from lingleo_client import GetLeoDict
from utils import shelve_get
from main_window import MainWindow


class Login(object):
    def __init__(self, root):
        self.root = root
        self.email = None
        self.password = None
        self.leo = GetLeoDict(self.email, self.password)

    def write

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('main_coordinates')
        return coordinates
