import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils import shelve_get, get_coordinates, shelve_delete, destroy


class MainWindow(object):
    def __init__(self, root, leo_obj):
        root.state = 'main'
        self.root = root
        self.leo = leo_obj
        self.words_state = self.leo.FILTER_ALL
        self.configure()
        self.create_menu()

    def configure(self):
        coordinates = get_coordinates('main', self.root)
        self.root.resizable(True, True)
        self.root.configure(background='#48B484')
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Logout', command=self.logout)
        file_menu.add_command(label='Exit', command=self.root.quit)
        file_menu.add_command(label='Save all words', command=self.save_words)
        words_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Words', menu=words_menu)

    def logout(self):
        shelve_delete('password')
        destroy(self.root)
        self.root.login_obj(self.root)

    def save_words(self):
        file_name = self.get_filename_to_save()
        if not file_name:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        with open(file_name, mode='w') as f:
            for leo_obj in getattr(self.leo, self.words_state):
                f.write(leo_obj['en_name'] + ' : ' + leo_obj['translated'])

    @staticmethod
    def get_filename_to_save():
        f = asksaveasfilename(confirmoverwrite=True, filetypes=(("All files", "*.txt"),),
                              defaultextension='.txt')
        return f
