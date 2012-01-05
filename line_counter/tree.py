
import os, re, operator
from file import File
from num import Num
from size import Size
from colors import Color

class Tree():
    def __init__(self, name, filters, afilters, settings):
        self.settings = settings
        self.in_byte = settings['size_in_byte']
        
        self.list_files = []
        self.list_folders = []
        self.name = name

        self.count_files = Num(0)
        self.count_folders = Num(0)
        self.total_lines = Num(0)
        self.total_size = Size(0, self.in_byte)

        self.global_count_files = Num(0)
        self.global_count_folders = Num(0)
        self.global_total_lines = Num(0)
        self.global_total_size = Size(0, self.in_byte)


        for f in os.listdir(self.name):
            #apply filters and afilters
            a = False
            for fl in filters:
                if re.match(fl, f):
                    a |= True

            a |= os.path.isdir(os.path.join(self.name, f))

            for af in afilters:
                if re.match(af, f):
                    a &= False
            
            if a == False:
                continue

            full_name = os.path.join(self.name, f)
            if os.path.isdir(full_name):
                self.list_folders.append(Tree(full_name, filters, afilters, settings))
                (n, f, d, l, s) = self.list_folders[-1].total()
                if f == 0 and d == 0:
                    self.list_folders.pop()
                    continue
                self.count_folders += Num(1)
                
                self.global_total_lines += l
                self.global_total_size += s
                self.global_count_files += f
                self.global_count_folders += d
            else:
                self.list_files.append(File(full_name, self.in_byte))
                (n, l, s) = self.list_files[-1].get()
                self.total_lines += l
                self.count_files += Num(1)
                self.total_size += s


    def get(self):
        return (self.name, self.count_files, self.count_folders, self.total_lines, self.total_size)

    def get_g(self):
        return (self.name, self.global_count_files, self.global_count_folders, self.global_total_lines, self.global_total_size)

    def total(self):
        return (self.name, self.global_count_files + self.count_files,
                self.global_count_folders + self.count_folders,
                self.global_total_lines + self.total_lines,
                self.global_total_size + self.total_size)

    def get_dict(self):
        l = []
        for f in self.list_files:
            fo = False
            for i in l:
                if i['ext'] == f.ext():
                    i['files'] += Num(1)
                    i['lines'] += f.line
                    i['size']  += f.size
                    fo = True
            if fo == False:
                l += [{'ext': f.ext(), 'files': Num(1), 'lines': f.line, 'size': f.size}]

        for d in self.list_folders:
            ll = d.get_dict()
            # merge 
            for d in ll:
                fo = False
                for g in l:
                    if d['ext'] == g['ext']:
                        g['lines'] += d['lines']
                        g['files'] += d['files'] 
                        g['size']  += d['size']
                        fo = True
                        break
                if fo == False:
                    l += [{'ext': d['ext'], 'files': d['files'], 'lines': d['lines'], 'size': d['size']}]

        return l

    def get_list(self):
        l = []

        for f in self.list_files:
            l.append( {'name' : f.name, 'line':f.line, 'size':f.size, 'ext':f.ext()} )

        for dir in self.list_folders:
            l += dir.get_list()

        return l

    def output(self, level = 0):
        color = Color(not self.settings['nocolor'])
        if self.settings['view'] == 'list':
            l = self.get_list()
            h_line = '|' + ('=' * (35)) + '|'
            style = '| {0:13} | {1:7} | {2:7} |'

            if len(l) > 0:
                l.sort(key=operator.itemgetter(self.settings['sort']))
                len_name = max(len(n['name']) for n in l)
                len_size = max(max(len(str(n['size'])) for n in l), 11)
                h_line = '|' + ('=' * (len_name + len_size + 19)) + '|'
                style = '| {0:' + str(len_name) + '} | {1!s:>11} | {2!s:>' + str(len_size) + '} |'

            print (h_line)
            print (style.format('name', 'lines', 'size'))
            print (h_line)

            for f in l:
                print (style.format(f['name'], str(f['line']), str(f['size'])))

            print (h_line)

        elif self.settings['view'] == 'tree':
            self.sort(self.settings)

            shift = '   ' * level

            if level == 0:
                print ('\n' + self.name)

            for d in self.list_folders:
                msg = shift + color.green() + '+- ' + color.blue() + os.path.basename(d.name) + color.end()
                if self.settings['folder'] == 'local':
                    (n, files, dirs, lines, size ) = d.get()
                    msg += ' ({0} files, {1} folders, {2} lines, {3})'.format(files, dirs, str(lines), str(size))
                if self.settings['folder'] == 'global':
                    (n, files, dirs, lines, size ) = d.get_g()
                    msg += ' ({0} files, {1} folders, {2} lines, {3})'.format(files, dirs, str(lines), str(size))

                if self.settings['folder'] == 'both':
                    (n1, f1, d1, l1, s1 ) = d.get()
                    (n2, f2, d2, l2, s2 ) = d.get_g()
                    msg += ' ({0} + {1} = {2} files, {3} + {4} = {5} folders, {6} + {7} = {8} lines, {9} + {10} = {11})'.format(f1, f2, f1 + f2, d1, d2, d1 + d2, str(l1), str(l2), str(l1 + l2), str(s1), str(s2), str(s1 + s2))

                print (msg)
                d.output(level+1)

            if len(self.list_files) > 0 and self.settings['hide_files'] == False:
                len_name = 3 * level + max(len(os.path.basename(n.name)) for n in self.list_files)            
                for f in self.list_files:
                    msg = shift + color.green() + '+-' + color.end() + ' {0:' + str(len_name) + '}' + color.gray() + ' ({1} lines, {2})' + color.end()
                    print msg.format(os.path.basename(f.name), str(f.line), str(f.size))


        ### stats
        if level == 0:
            if self.settings['stats'] in ['short', 'all']:
                (n, f, d, l, s) = self.total()
                print ('\nstatistics:')
                print ('\tfolders  : '+ str(d))
                print ('\tfiles    : '+ str(f))
                print ('\tlines    : '+ str(l))
                print ('\tsize     : '+ str(s))

            if self.settings['stats']  == 'all':
                le = self.get_dict()
                print ('\nby extention:')
                for e in le:
                    print ("{0!s:>8}".format(e['ext']) + ' : ' + "{0!s:>10}".format(str(e['files'])) + ' files; ' + "{0!s:>12}".format(str(e['lines'])) + ' lines ' + "{0!s:>12}".format(str(e['size'])))

    def sort(self, settings):
        s = settings['sort']
        if (s == "name"):
            self.list_files.sort(key=lambda x: x.name)
            self.list_folders.sort(key=lambda x: x.name)
        if (s == "line"):
            self.list_files.sort(key=lambda x: int(x.line))
            self.list_folders.sort(key=lambda x: int(x.global_total_lines))
        if (s == "size"):
            self.list_files.sort(key=lambda x: int(x.size))
            self.list_folders.sort(key=lambda x: int(x.global_total_size))
        if (s == "ext"):
            self.list_files.sort(key=lambda x: x.ext())

        for dir in self.list_folders:
            dir.sort(settings)

