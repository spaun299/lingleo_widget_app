import shelve
import os


def shelve_get(keys):
    ret = dict()
    shelve_file = shelve.open(os.path.join('shelve_session'))
    for key in keys:
        ret[key] = shelve_file.get(key)
    return ret


def shelve_save(**kwargs):
    shelve_file = shelve.open(os.path.join('shelve_session'), writeback=True)
    print(kwargs)
    for k, v in kwargs.items():
        shelve_file[k] = v


def get_coordinates(window):
    key = '%s_coordinates' % window
    return shelve_get([key, ])[key]
