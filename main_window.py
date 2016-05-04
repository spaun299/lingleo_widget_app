import tkinter as tk
from utils import shelve_get, get_coordinates


class MainWindow(object):
    def __init__(self, root, leo_obj):
        root.state = 'main'
        self.root = root
        self.leo = leo_obj

    def configure(self):
        coordinates = get_coordinates('main', self.root)
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))
