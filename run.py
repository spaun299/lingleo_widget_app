import tkinter
from config import app_name
from main import Main
from login_window import Login
import os
from utils import documents_folder, get_folder_path_in_documents


def root():
    master = tkinter.Tk(screenName=app_name,
                        baseName=app_name, className=app_name)
    master.login_obj = Login
    Main(master)

    return master


if __name__ == '__main__':
    doc_folder = documents_folder()
    leo_folder = get_folder_path_in_documents()
    if not os.path.exists(doc_folder):
        os.makedirs(doc_folder)
    if not os.path.exists(leo_folder):
        os.makedirs(leo_folder)
    main = root()
    main.mainloop()
