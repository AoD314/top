
class Num():
    def __init__(self, num):
        self.num = int(num)

    def __add__(self, num):
        return Num(self.num + int(num))

    def __int__(self):
        return int(self.num)

    def __eq__(self, value):
        return True if int(self.num) == int(value) else False

    def __lt__(self, value):
        return True if int(self.num) < int(value) else False

    def __str__(self):
        return (format(self.num, "1,d").replace(",", " "))    

