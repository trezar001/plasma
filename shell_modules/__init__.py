#put all your modules here or they won't work nicely!

import shell_modules.sample as sample
import shell_modules.upgrade as upgrade


def get_modules():
     return [sample, upgrade]