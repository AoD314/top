import re
import glob

def is_standard(name):
    return True if name in [
        '__future__',
        'Queue',
        'abc',
        'argparse',
        'base64',
        'calendar',
        'collections',
        'copy',
        'datetime',
        'email',
        'functools',
        'gc',
        'glob',
        'hashlib',
        'inspect',
        'io',
        'json',
        'logging',
        'multiprocessing',
        'operator',
        'os',
        'random',
        're',
        'shutil',
        'socket',
        'sqlite3',
        'stat',
        'subprocess',
        'sys',
        'tempfile',
        'threading',
        'time',
        'timeit',
        'traceback',
        'urlparse',
        'warnings',
        'xml'
    ] else False

def read_text(path):
    text = []
   
    with open(path, 'r') as file:
        text = file.readlines()

    return text

def filter(line):
    im = re.compile('import (.*)')
    fr = re.compile('from (\w+) .*')
    fn = re.compile('.*def (\w+)\(.*')

    if not fr.match(line) is None:
        return fr.match(line).group(1)
    elif not im.match(line) is None:
        return im.match(line).group(1)
    return None

def filter_fn(line):
    fn = re.compile('.*def (\w+)\(.*')

    if not fn.match(line) is None:
        name = fn.match(line).group(1)
        if name[0] == '_':
            return None
        else:
            return name
    return None

def get_modules(filename):

    text = read_text(filename)

    modules = []
    fns = []

    for i, line in enumerate(text):
        line = line.strip()
        out = filter(line)
        fn = filter_fn(line)

        if not fn is None:
            if not out in fns:
                fns.append(fn)

        if out is None:
            continue

        if ' ' in out:
            out = out.split(' ')[0]

        if '.' in out:
            out = out.split('.')[0]

        if not is_standard(out):
            if not out in modules:
                modules.append(out)

    if len(modules) + len(fns) == 0:
        return None

    return {'name': filename, 'mods': modules, 'fns': fns}

def main():
    all_modules = []

    path = './**/*.py'

    for name in glob.glob(path, recursive=True):
        module = get_modules(name)
        if module is not None:
            all_modules.append(module)

    for m in all_modules:
        print(m['name'])
        print('modules:')
        for i in m['mods']:
            print('    ' + str(i))
        print('functions:')
        for f in m['fns']:
            print('    ' + str(f))
        print(' ')

    print('Total files: {}'.format(len(all_modules)))

if __name__ == '__main__':
    main()