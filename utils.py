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
    for kwarg in kwargs:
        shelve_file[kwarg] = kwargs[kwarg]
