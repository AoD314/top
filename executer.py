#!/usr/bin/env python3

import re
import subprocess
import argparse
import os
import multiprocessing
from multiprocessing import Lock
from threading import Thread


def read_cmd_from_file(name):
    with open(name, 'rt') as f:
        text = f.read()
    l = text.split('\n')
    nl = []
    for c in l:
        if re.match('^[\t ]*[^#]*(.*)', c).groups()[0] == '':
            cmd = c.strip()
            if cmd != '':
                nl.append(cmd)
    return nl


cmd = []
lock = Lock()


def get_cmd():
    global cmd
    c = ''
    with lock:
        if len(cmd) > 0:
            c = cmd[0]
            cmd = cmd[1:]
            print('estimated tasks: ', len(cmd))
    return c


def run_cmd():
    c = get_cmd()
    while c != '':
        subprocess.getoutput(c)
        c = get_cmd()


def main(np, files):
    global cmd
    for name in files:
        cmd = read_cmd_from_file(name)

        pool = []
        for i in range(np):
            t = Thread(target=run_cmd, daemon=True)
            pool += [t]
            t.start()

        for p in pool:
            p.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run command from files in parallel.')
    parser.add_argument('-j', type=int, default=0, help='amount of parallel processes')
    parser.add_argument('file', metavar='file', type=str, nargs='+', help='file with commands')

    args = parser.parse_args()

    np = args.j if args.j != 0 else multiprocessing.cpu_count()

    files = [f for f in sorted(set(args.file)) if os.path.isfile(f)]
    if 0 < np < 4096 and len(files) > 0:
        main(np, files)
