from login_window import Login
from main_window import MainWindow
from utils import shelve_get, shelve_save, get_coordinates
from lingleo_client import GetLeoDict
from list_window import ListWindow


class Main(object):
    def __init__(self, root):
        self.root = root
        self.user_credentials = self.get_user_credentials()
        self.leo = GetLeoDict(**self.user_credentials)
        self.authorized = self.leo.authorized
        self.last_program_state = self.last_program_state()
        self.configure()
        if not self.authorized:
            Login(self.root)
        elif self.last_program_state == 'list':
            ListWindow(self.root, self.leo)
        else:
            MainWindow(self.root, self.leo)

    @staticmethod
    def get_user_credentials():
        return shelve_get(['email', 'password'])

    @staticmethod
    def last_program_state():
        state = shelve_get(['last_state'])
        if state:
            state = state['last_state']
        else:
            state = 'main'
        return state

    def on_closing(self):
        params = dict(last_state=self.root.state)
        coordinates = {'x': self.root.winfo_rootx(),
                       'y': self.root.winfo_rooty(),
                       'w': self.root.winfo_width(),
                       'h': self.root.winfo_height()}
        if self.root.state == 'main':
            params['main_coordinates'] = coordinates
        elif self.root.state == 'list':
            params['list_coordinates'] = coordinates
        shelve_save(**params)
        self.root.destroy()

    def configure(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
