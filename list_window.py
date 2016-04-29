import tkinter as tk
from utils import shelve_get


class ListWindow(object):
    def __init__(self, root, leo_obj):
        self.root = root
        self.leo = leo_obj
        self.coordinates = self.get_canvas_coordinates()

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('list_coordinates')
        return coordinates
