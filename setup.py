import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable('run.py', base=base,
                                    targetName="LingleoWidget.exe",
                                    icon="favicon.ico")]
cx_Freeze.setup(
    name='LingleoWidget',
    version="0.1",
    options={'build_exe': {'packages': ['PIL', 'dbm'],
                           'include_files': ['background_login.jpg',
                                             'favicon.ico',
                                             'shelve_session.bak',
                                             'shelve_session.dat',
                                             'shelve_session.dir']}},
    executables=executables
)
