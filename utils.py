import shelve
import os
import config
import tkinter as tk


def documents_folder():
    return os.path.expanduser('~/Documents')


def get_folder_path_in_documents(folder='LingLeo'):
    return documents_folder() + '/' + folder


# def get_file_path_in_documents(file_name):
#     focuments_folder = os.path.expanduser('~/Documents')
#     path = []
#     found = False
#     for name in reversed(os.path.dirname(os.path.abspath(__file__)).split('\\')):
#         if config.app_name.replace(' ', '') == path or found:
#             path.append(name)
#     return '\\'.join(path) + '\\' + file_name


def shelve_get(keys):
    ret = dict()
    shelve_file = shelve.open(
        get_folder_path_in_documents() + '/' + 'shelve_session')
    for key in keys:
        ret[key] = shelve_file.get(key)
    return ret


def shelve_delete(key):
    shelve_file = shelve.open(
        shelve.open(get_folder_path_in_documents() + '/' + 'shelve_session'),
        writeback=True)
    del shelve_file[key]


def shelve_save(**kwargs):
    shelve_file = shelve.open(
        get_folder_path_in_documents() + '/' + 'shelve_session',
        writeback=True)
    for k, v in kwargs.items():
        shelve_file[k] = v


def get_coordinates(window, root):
    key = '%s_coordinates' % window
    coordinates = shelve_get([key, ])
    if coordinates.get('main_coordinates'):
        coordinates = coordinates[key]
    else:
        coordinates = {'x': (root.winfo_screenwidth() / 2) - (config.WIDTH_DEFAULT / 2),
                       'y': (root.winfo_screenheight() / 2) - (config.HEIGHT_DEFAULT / 2),
                       'w': config.WIDTH_DEFAULT, 'h': config.HEIGHT_DEFAULT}
    return coordinates


def create_text(root, x, y, text, anchor='nw'):
    txt = root.create_text(x, y, anchor=anchor, font=root.master.font)
    root.itemconfig(txt, text=text)


def destroy(root):
    for child in root.winfo_children():
        child.destroy()
