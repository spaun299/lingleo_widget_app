import tkinter
from config import app_name
from main import Main


def root():
    master = tkinter.Tk(screenName=app_name)
    Main(master)
    return master

if __name__ == '__main__':
    root().mainloop()
