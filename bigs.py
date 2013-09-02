#!/usr/bin/env python3

import os
import sys

def size_to_str(size):
    # B-> K -> M -> G -> T
    s = [" B", " K", " M", " G", " T", " P", " E", " Z", " Y"]

    for i in range(len(s)):
        if size <= 9999:
            j = len(str(int(size)))
            f = ''
            if (2-j >= 0) and i != 0:
                f = "{" + ":.{0}f".format(3-j) + "}"
            else:
                f = "{0:4}"
                size = int(size)
            size_s = f.format(size) + s[i]
            return size_s
        size /= 1000.0

def main(path):
    dic = []
    files = os.listdir(path)
    total_s = 0
    for f in files:
        full_name = os.path.join(path, f)
        sz = int(os.path.getsize(full_name))
        total_s += sz
        dic += [{'name': f, 'size': sz}]
    dic.sort(key=lambda x: -x['size'])

    print(path + ' : ' + size_to_str(total_s))
    for i in dic[:50]:
        print("{0}    {1}".format(size_to_str(i['size']), i['name']))

if __name__ == '__main__':
    d = os.getcwd()
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        d = sys.argv[1]
    main(d)

