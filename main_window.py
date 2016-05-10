import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from utils import shelve_get, get_coordinates, shelve_delete, destroy
from tkinter.messagebox import showinfo
import config


class MainWindow(object):
    def __init__(self, root, leo_obj):
        root.state = 'main'
        self.root = root
        self.leo = leo_obj
        self.words_state = self.leo.STATE_ALL
        self.statusbar = None
        self._last_action = 'Logged in'
        self.configure()
        self.create_menu()
        self.create_statusbar()

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, action):
        self.change_statusbar_message(last_action=action)

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
        save_menu = tk.Menu(file_menu, tearoff=False)
        file_menu.add_cascade(label='Save to computer', menu=save_menu)
        save_menu.add_command(label='All words',
                              command=lambda: self.save_words(self.leo.STATE_ALL))
        save_menu.add_command(label='Learning words',
                              command=lambda: self.save_words(self.leo.STATE_LEARNING))
        save_menu.add_command(label='Learned words',
                              command=lambda: self.save_words(self.leo.STATE_LEARNED))
        save_menu.add_command(label='New words',
                              command=lambda: self.save_words(self.leo.STATE_NEW))
        file_menu.add_separator()
        file_menu.add_command(label='Logout', command=self.logout)
        file_menu.add_command(label='Exit', command=self.root.quit)
        words_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Words', menu=words_menu)

    def logout(self):
        shelve_delete('password')
        destroy(self.root)
        self.root.login_obj(self.root)

    def save_words(self, words_state=None):
        file_name = self.get_filename_to_save()
        words_state = words_state or self.words_state
        if not file_name:
            return
        with open(file_name, mode='w') as f:
            for leo_obj in getattr(self.leo, words_state):
                f.write(leo_obj['en_name'].capitalize() +
                        ' : ' +
                        leo_obj['translated'].capitalize() + '\n')
        showinfo(config.app_name, 'Saved successfully',
                 type='ok', icon='info')
        self.last_action = 'File saved'

    @staticmethod
    def get_filename_to_save():
        f = asksaveasfilename(confirmoverwrite=True,
                              filetypes=(("All files", "*.txt"),),
                              defaultextension='.txt')
        return f

    def create_statusbar(self):
        statusbar = tk.Label(self.root, text=self.statusbar_message(last_action='Logged in'),
                             bd=1, relief=tk.SUNKEN,
                             anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.statusbar = statusbar

    def change_statusbar_message(self, message='', last_action=''):

        self.statusbar.configure(text=self.statusbar_message(message,
                                                             last_action))

    def statusbar_message(self, message='', last_action=''):
        words_count = len(getattr(self.leo, self.words_state))
        last_action = 'Last action: %s' % last_action
        return '%s\t\t%s : %s\t\t%s' % (last_action,
                                        self.leo.STATE_READABLE[self.words_state],
                                        words_count,
                                        message)
