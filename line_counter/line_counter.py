#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, argparse, operator

########################################################################################################################

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

########################################################################################################################

def len_to_str(value):
	return (format(value, "1,d").replace(",", " "))    

def size_to_str(size, in_byte):
    if in_byte == True:
        return str(size)
    else:
        if int(size) < 1024:
            return str(size) + '  B'
         
        suf = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
        for i in xrange(len(suf)):
            if int(size) > (1024 ** (i + 1)):
                continue
            else:
                msg = "{0:.2f} " + suf[i - 1]
                return msg.format(float(size) / (1024 ** i))

########################################################################################################################

class Tree():
    def __init__(self, name, filters, settings):
        self.settings = settings
        self.list_files = []
        self.list_folders = []
        self.name = name
        self.count_files = 0
        self.count_folders = 0
        self.total_lines = 0
        self.total_size = 0
        self.global_count_files = 0
        self.global_count_folders = 0
        self.global_total_lines = 0
        self.global_total_size = 0

        for f in os.listdir(self.name):
            full_name = os.path.join(self.name, f)
            if os.path.isdir(full_name):
                if f[0] == '.':
                    continue
                self.list_folders.append(Tree(full_name, filters, settings))
                (n, f, d, l, s) = self.list_folders[-1].get_g()
                if f == 0 and d == 0:
                    self.list_folders.pop()
                    continue
                self.global_total_lines += l
                self.global_total_size += s
                self.count_folders += 1
                self.global_count_files += f
                self.global_count_folders += d
            else:
                # check filters
                f = False
                for ext in filters:
                    if full_name.split('.')[-1] == ext:
                        f = True
                if f == False:
                    continue
                self.list_files.append(File(full_name))
                (n, l, s) = self.list_files[-1].get()
                self.total_lines += l
                self.total_size += s
                self.count_files += 1

    def get(self):
        return (self.name, self.count_files, self.count_folders, self.total_lines, self.total_size)

    def get_g(self):
        return (self.name,
                self.global_count_files + self.count_files,
                self.global_count_folders + self.count_folders,
                self.global_total_lines + self.total_lines,
                self.global_total_size  + self.total_size)
        
    def get_dict(self):
        l = []
        for f in self.list_files:
            fo = False
            for i in l:
                if i['ext'] == f.ext():
                    i['files'] += 1
                    i['lines'] += f.line
                    i['size']  += f.size
                    fo = True
            if fo == False:
                l += [{'ext': f.ext(), 'files': 1, 'lines': f.line, 'size': f.size}]
            
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
                print (style.format(f['name'], len_to_str(f['line']), size_to_str(f['size'], self.settings['size_in_byte'])))
                    
            print (h_line)
            
        elif self.settings['view'] == 'tree':
            self.sort(self.settings)
            
            shift = '   ' * level
            
            if level == 0:
                print ('\n' + self.name)
            
            for d in self.list_folders:
                msg = shift + '+- ' + bcolors.OKBLUE + os.path.basename(d.name) + bcolors.ENDC
                if self.settings['folder'] == 'local':
                    (n, files, dirs, lines, size ) = d.get()
                    msg += ' ({0} files, {1} folders, {2} lines, {3})'.format(files, dirs, len_to_str(lines), size_to_str(size, self.settings['size_in_byte']))
                if self.settings['folder'] == 'global':
                    (n, files, dirs, lines, size ) = d.get_g()
                    msg += ' ({0} files, {1} folders, {2} lines, {3})'.format(files, dirs, len_to_str(lines), size_to_str(size, self.settings['size_in_byte']))

                if self.settings['folder'] == 'both':
                    (n1, f1, d1, l1, s1 ) = d.get()
                    (n2, f2, d2, l2, s2 ) = d.get_g()
                    msg += ' ({0}+{1}={2} files, {3}+{4}={5} folders, {6}+{7}={8} lines, {9}+{10}={11})'.format(f1, f2, f1+f2, d1, d2, d1+d2, len_to_str(l1), len_to_str(l2), len_to_str(l1+l2), size_to_str(s1, self.settings['size_in_byte']), size_to_str(s2, self.settings['size_in_byte']), size_to_str(s1 + s2, self.settings['size_in_byte']) )
                    
                print (msg)
                d.output(level+1)
            
            if len(self.list_files) > 0 and self.settings['hide_files'] == False:
                len_name = 3 * level + max(len(os.path.basename(n.name)) for n in self.list_files)            
                for f in self.list_files:
                    msg = shift + '+- {0:' + str(len_name) + '} ({1} lines, {2})'
                    print msg.format(os.path.basename(f.name), len_to_str(f.line), size_to_str(f.size, self.settings['size_in_byte']))
            
            
        ### stats
        if level == 0:
            if self.settings['stats'] in ['short', 'all']:
                (n, f, d, l, s) = self.get_g()
                print ('\nstatistics:')
                print ('\tfolders  : '+ str(d))
                print ('\tfiles    : '+ str(f))
                print ('\tlines    : '+ str(len_to_str(l)))
                print ('\tsize     : '+ str(size_to_str(s, self.settings['size_in_byte'])))
                
            if self.settings['stats']  == 'all':
                le = self.get_dict()
                print ('\nby extention:')
                for e in le:
                    print ("{0!s:>8}".format(e['ext']) + ' : ' + "{0!s:>10}".format(len_to_str(e['files'])) + ' files; ' + "{0!s:>12}".format(len_to_str(e['lines'])) + ' lines ' + "{0!s:>12}".format(size_to_str(e['size'], self.settings['size_in_byte'])))
                
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
        

########################################################################################################################

class File():
    def __init__(self, name):
        self.name = name
        self.line = 0
        self.size = 0
        try:
            self.line = sum(1 for l in open(name))
            self.size = os.path.getsize(name)
        except:
            pass

    @property
    def name(self):
        return self.name

    @property
    def line(self):
        return self.line

    @property
    def size(self):
        return self.size

    def ext(self):
        return self.name.split('.')[-1]

    def get(self):
        return (str(self.name), int(self.line), int(self.size))
    
    def __getitem__(self):
        return self

########################################################################################################################

def analyze(settings):
    start_time = time.time()
    
    fltrs = settings['filters']
    #print ('filters  : ' + str(fltrs))  
    
    if 'cpp' in settings['code']:
        fltrs += ['cpp', 'c++', 'hpp', 'h', 'h++']

    if 'c' in settings['code']:
        fltrs += ['c', 'cc', 'h']
    
    if 'cmake' in settings['code']:
        fltrs += ['CMakeLists.txt', 'cmake', 'cmake.in']

    if 'py' in settings['code']:
        fltrs += ['py']

    if 'tex' in settings['code']:
        fltrs += ['tex']

    if 'cs' in settings['code']:
        fltrs += ['cs']

    if 'web' in settings['code']:
        fltrs += ['html', 'htm', 'css', 'js']

    if 'php' in settings['code']:
        fltrs += ['php']

    #print ('settings : ' + str(settings))
    #print ('filters  : ' + str(fltrs))

    tree = Tree(settings['path'], fltrs, settings)
    tree.output()
    
    time_sec = time.time() - start_time
    print ("\nanalyze time : {0:2.5f}sec".format(time_sec))

def main():
    parser = argparse.ArgumentParser(description='Line Counter')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--hide-files', action='store_true', help='help')
    parser.add_argument('-p', '--path', help='path to directory with sources codes', default='.')
    parser.add_argument('--size-in-byte', action='store_true', help='show size in byte')
    parser.add_argument('-f', '--filters', nargs='*', help='list of filters', default=[''], metavar='F')
    parser.add_argument('-v', '--view', choices=['tree', 'list'], default='tree', help='set view for display output(default: %(default)s)')
    parser.add_argument('--stats', choices=['none', 'short', 'all'], default='short', help='display statistics by code (default: %(default)s)')
    parser.add_argument('-s', '--sort', choices=['name', 'line', 'size', 'ext'], default='name', help='sort of the results(default: %(default)s)')
    parser.add_argument('--folder', choices=['none', 'local', 'global', 'both'], default='both', help='print info about directory(default: %(default)s)')
    parser.add_argument('-c', '--code', nargs='+', choices=['cpp', 'c', 'tex', 'cmake', 'py', 'cs', 'web', 'php'], default=[''], help='print info about directory(default: %(default)s)')
    parser.add_argument('--examples', action='store_true', help="print several examples")
    parser.add_argument('--nocolor',  action='store_true', help="use only white/black color for display all text")
   
    analyze(vars(parser.parse_args()))

if __name__ == "__main__":
    main()




