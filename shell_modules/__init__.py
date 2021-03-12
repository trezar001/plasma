#put all your modules here or they won't work nicely!

import shell_modules.sample as sample
import shell_modules.pshell_download as pshell_download
import shell_modules.tty_shell as tty

def get_modules():
     return [sample, pshell_download, tty]