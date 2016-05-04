import shelve
import os
import config


def shelve_get(keys):
    ret = dict()
    shelve_file = shelve.open('%s\shelve_session' % os.path.dirname(
        os.path.abspath(__file__)))
    for key in keys:
        ret[key] = shelve_file.get(key)
    return ret


def shelve_save(**kwargs):
    shelve_file = shelve.open('%s\shelve_session' % os.path.dirname(
        os.path.abspath(__file__)), writeback=True)
    for k, v in kwargs.items():
        shelve_file[k] = v


def get_coordinates(window, root):
    key = '%s_coordinates' % window
    coordinates = shelve_get([key, ])
    if coordinates:
        coordinates = coordinates[key]
    else:
        coordinates = {'x': (root.winfo_screenwidth() / 2) - (config.WIDTH_DEFAULT / 2),
                       'y': (root.winfo_screenheight() / 2) - (config.HEIGHT_DEFAULT / 2),
                       'w': config.WIDTH_DEFAULT, 'h': config.HEIGHT_DEFAULT}
    return coordinates
