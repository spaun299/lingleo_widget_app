import tkinter as tk
from lingleo_client import GetLeoDict
from utils import shelve_get, shelve_save, create_text, destroy
from main_window import MainWindow
import config
import os
from PIL import Image, ImageTk
import time
from tkinter.messagebox import showinfo


class Login(object):
    def __init__(self, root):
        root.state = 'main'
        self.root = root
        self.email = None
        self.password = None
        self.canvas = None
        self.configure()
        self.write_canvas()
        self.loading = False

    def write_canvas(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.write_background(self.canvas)
        create_text(self.canvas, 55, 30, 'Name')
        create_text(self.canvas, 50, 80, 'Password')
        create_text(self.canvas, 100, 5, 'Login to lingualeo')
        email_text = tk.StringVar(value="Email")
        password_text = tk.StringVar(value="Password")
        self.email = tk.Entry(self.canvas, textvariable=email_text, width=15, bg='white',
                              fg='gray', font=self.root.font)
        self.email.bind("<FocusIn>", lambda e: self.make_empty_field('email'))
        self.email.bind("<FocusOut>", lambda e: self.fill_field('email'))
        self.email.bind('<Return>', lambda e: self.login())
        self.email.grid(pady='30', padx='135', row=1, column=0)
        self.password = tk.Entry(self.canvas, textvariable=password_text, width=15, bg='white',
                                 font=self.root.font, fg='gray')
        self.password.bind("<FocusOut>", lambda e: self.fill_field('password'))
        self.password.bind("<FocusIn>", lambda e: self.make_empty_field('password'))
        self.password.bind('<Return>', lambda e: self.login())
        self.password.grid(pady='0', padx='0', row=2, column=0)
        submit = tk.Button(self.canvas, text='Login', bg='#F4D03F', width=20,
                           font=self.root.font, command=self.login)
        submit.grid(pady='10', padx='0', row=3, column=0)

    def login(self):
        self.loading = True
        self.root.after(0, self.run_loading)
        email = self.email.get()
        password = self.password.get()
        leo = GetLeoDict(email, password)
        self.loading = False
        if not leo.authorized:
            showinfo(config.app_name, 'Email or password incorrect',
                     type='ok', icon='warning')
            return
        shelve_save(email=email, password=password)
        destroy(self.root)
        MainWindow(self.root, leo)

    def run_loading(self, dot='', delete_id=None):
        try:
            loading = 'Loading'
            if delete_id:
                self.canvas.delete(delete_id)
            txt = self.canvas.create_text(27, 115, anchor='nw', font=('Helvetica', '11', 'bold'))
            self.canvas.itemconfig(txt, text=loading + dot)
            dot = dot + '.' if len(dot) < 3 else ''
            if self.loading:
                self.root.after(500, self.run_loading, dot, txt)
            elif not delete_id:
                self.root.after(200, self.run_loading, dot, txt)
            else:
                self.canvas.delete(txt)
        except tk.TclError:
            pass

    @staticmethod
    def write_background(canvas):
        background_image = Image.open(os.path.join(config.BACKGROUND_IMAGE_LOGIN))
        tkimage = ImageTk.PhotoImage(background_image)
        canvas.img = tkimage
        canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)

    def configure(self):
        coordinates = {'x': (self.root.winfo_screenwidth() / 2) - (config.WIDTH_SMALL_DEFAULT / 2),
                       'y': (self.root.winfo_screenheight() / 2) - (config.HEIGHT_SMALL_DEFAULT / 2),
                       'w': config.WIDTH_SMALL_DEFAULT, 'h': config.HEIGHT_SMALL_DEFAULT}
        self.root.geometry('%dx%d+%d+%d' % (coordinates['w'], coordinates['h'],
                                            coordinates['x'], coordinates['y']))
        self.root.resizable(False, False)

    def make_empty_field(self, event):
        obj = getattr(self, event)
        if obj.get().lower() == event:
            obj.delete(0, tk.END)
            obj.insert(0, '')
            params = dict(fg='black')
            if event == 'password':
                params.update(show='*')
            obj.configure(**params)

    def fill_field(self, event):
        obj = getattr(self, event)
        if not obj.get():
            obj.insert(0, event.capitalize())
            params = dict(fg='gray')
            if event == 'password':
                params.update(show='')
            obj.configure(**params)

    @staticmethod
    def get_canvas_coordinates():
        coordinates = shelve_get('main_coordinates')
        return coordinates
