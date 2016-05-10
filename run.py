import tkinter
from config import app_name
from main import Main
from login_window import Login


def root():
    master = tkinter.Tk(screenName=app_name, baseName=app_name, className=app_name)
    master.login_obj = Login
    Main(master)

    return master


if __name__ == '__main__':
    main = root()
    main.mainloop()
