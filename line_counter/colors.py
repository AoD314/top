
import sys

class Color():
    def __init__(self, c = True):
        self.is_c = c
        pass

    def blue(self):
        if (sys.platform == 'linux2' or sys.platform == 'linux3') and self.is_c == True:
            return '\033[1;94m'
        else:
            return ''
    
    def green(self):
        if (sys.platform == 'linux2' or sys.platform == 'linux3') and self.is_c == True:
            return '\033[1;32m'
        else:
            return ''
    
    def gray(self):
        if (sys.platform == 'linux2' or sys.platform == 'linux3') and self.is_c == True:
            return '\033[1;30m'
        else:
            return ''
    
    def end(self):
        if (sys.platform == 'linux2' or sys.platform == 'linux3') and self.is_c == True:
            return '\033[0m'
        else:
            return ''
