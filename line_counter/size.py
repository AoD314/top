
from num import Num

class Size():
    def __init__(self, s, in_byte = True):
        self.size = int(s)
        self.in_byte = in_byte
    
    def __add__(self, s):
        return Size(self.size + int(s), self.in_byte)

    def __int__(self):
        return int(self.size)

    def __lt__(self, value):
        return int(self.size) < int(value)

    def __str__(self):
        if self.in_byte == True:
            return str(Num(self.size))
        else:
            if int(self.size) < 1024:
                return str(self.size) + '  B'

        suf = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
        d = 0
        for i in range(len(suf)):
            if int(self.size) > (1024 ** (i + 1)):
                d = i + 1
                continue
            else:
                msg = "{0:.2f} " + suf[d - 1]
                break

        return msg.format(float(self.size) / (1024 ** d))

