import os
from num import Num
from size import Size

class File():
    def __init__(self, name, in_byte):
        self.n = name
        self.line = Num(0)
        self.size = Size(0, in_byte)
        try:
            self.line = Num(sum(1 for l in open(name)))
            self.size = Size(os.path.getsize(name), in_byte)
        except:
            pass

    @property
    def name(self):
        return self.n

    def ext(self):
        return self.name.split('.')[-1]

    def get(self):
        return (self.name, self.line, self.size)

    def __getitem__(self):
        return self
