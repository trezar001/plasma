import sys
from cx_Freeze import setup, Executable

include_files = []
build_exe_options = {'packages': [], 'include_files': include_files}

base = None

if sys.platform == 'win32':
    #base = 'Win32GUI'
    base = 'Console'

if sys.platform == 'win64':
    #base = 'Win64GUI'
    base = 'Console'

setup(name='plasma_client',
      version='1.0',
      description='plasma client',
      options={'build_exe': build_exe_options},
      executables=[Executable('server.py',base=base), Executable('client.py',base=base)])
