from login_window import Login
from main_window import MainWindow
from utils import shelve_get
from lingleo_client import GetLeoDict
from list_window import ListWindow


class Main(object):
    def __init__(self, root):
        self.root = root
        self.user_credentials = self.get_user_credentials()
        self.leo = GetLeoDict(**self.user_credentials)
        self.authorized = self.leo.authorized
        self.last_program_state = self.last_program_state
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
    def last_program_state(self):
        state = shelve_get(['last_state'])
        return state
