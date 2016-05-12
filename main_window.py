import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from utils import shelve_get, get_coordinates, shelve_delete, destroy, create_text
from tkinter.messagebox import showinfo
import config


class MainWindow(object):
    def __init__(self, root, leo_obj):
        root.state = 'main'
        self.root = root
        self.leo = leo_obj
        self.words_state = self.leo.STATE_ALL
        self.statusbar = None
        self.frame = None
        self.canvas = None
        self.canvas_size = None
        self.scrollbar = None
        self.words_canvas_text = None
        self._last_action = 'Logged in'
        self.configure()
        self.create()

    def create(self):
        self.create_menu()
        self.create_statusbar()
        self.create_toolbar()
        self.main_window()

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

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=0, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.font = self.root.font
        canvas = tk.Canvas(toolbar, background='#019875',
                           height=20, highlightthickness=0)
        canvas.pack(expand=True, fill=tk.X)

        create_text(canvas, 70, 2, 'English word')
        create_text(canvas, 400, 2, 'Translated word')
        canvas.create_line(395, 0, 395, 20, fill='#43A579')
        canvas.create_line(0, 19, 9999, 19, fill='#43A579')

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
        words_menu.add_command(label='All words', command=self.main_window)
        words_menu.add_command(label='New words',
                               command=lambda: self.main_window(
                                   words_state=self.leo.STATE_NEW))
        words_menu.add_command(label='Learned words',
                               command=lambda: self.main_window(
                                   words_state=self.leo.STATE_LEARNED))
        words_menu.add_command(label='Learning words',
                               command=lambda: self.main_window(
                                   words_state=self.leo.STATE_LEARNING))

    def main_window(self, words_state='all_words'):
        self.words_state = words_state
        new = True
        y = 0
        words = getattr(self.leo, self.words_state)
        if self.frame:
            new = False
            self.canvas.destroy()
        else:
            self.frame = tk.Frame(self.root, bd=0)
            self.frame.font = self.root.font
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
            self.scrollbar = tk.Scrollbar(self.frame)
            self.scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.canvas_size = len(words) * 30
        self.canvas = tk.Canvas(self.frame, bd=0, background=self.root['background'],
                                scrollregion=(0, 0, 0, len(words) * 30),
                                yscrollcommand=self.scrollbar.set,
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        def _on_mousewheel(event):

            if self.canvas_size > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.root.bind_all("<MouseWheel>", _on_mousewheel)

        for count, word in enumerate(words, start=1):
            if len(word['en_name']) > 40:
                word['en_name'] = word['en_name'][:40]
            create_text(self.canvas, 20, y, count)
            create_text(self.canvas, 70, y, word['en_name'])
            create_text(self.canvas, 400, y, word['translated'])
            self.canvas.create_line(0, y-8, 9999, y-8, fill='#43A579')
            y += 30
        self.canvas.create_line(60, 0, 60, len(words) * 30, fill='#43A579')
        self.canvas.create_line(395, 0, 395, len(words) * 30, fill='#43A579')
        self.scrollbar.config(command=self.canvas.yview)
        if new:
            self.frame.pack(expand=True, fill=tk.BOTH)

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
