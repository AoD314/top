

class Filters():
    def __init__(self, code, filtrs):
        self.c = code
        self.f = filtrs

    def filters(self):
        fltrs = []
        if 'cpp' in self.c:
            fltrs += ['.+\.cpp$', '.+\.c\+\+$', '.+\.hpp$', '.+\.h$', '.+\.h\+\+$']

        if 'c' in self.c:
            fltrs += ['.+\.c$', '.+\.cc$', '.+\.h$']

        if 'cmake' in self.c:
            fltrs += ['^CMakeLists\.txt$', '.+\.cmake$', '.+\.cmake\.in$']

        if 'py' in self.c:
            fltrs += ['.+\.py$']

        if 'tex' in self.c:
            fltrs += ['.+\.tex$']

        if 'd' in self.c:
            fltrs += ['.+\.d$']

        if 'cs' in self.c:
            fltrs += ['.+\.cs$']

        if 'web' in self.c:
            fltrs += ['.+\.html$', '.+\.htm$', '.+\.css$', '.+\.js$', '.+\.php$']

        if 'java' in self.c:
            fltrs += ['.+\.java$']

        if 'php' in self.c:
            fltrs += ['.+\.php$']

        if len(self.f) > 0:
            fltrs += self.f

        return fltrs

