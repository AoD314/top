#!/usr/bin/env python3

import re
import subprocess
import argparse
import os
import multiprocessing
from multiprocessing import Lock
from threading import Thread

import time

import datetime

run_status = {}


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


def status_thread():
    while True:
        time.sleep(60)
        with open('status_executer.log', 'w') as f:
            for k in run_status.keys():
                f.write('{}: [{}]\n'.format(k, run_status[k]))
                f.flush()


def get_cmd():
    global cmd
    c = ''
    with lock:
        if len(cmd) > 0:
            c = cmd[0]
            cmd = cmd[1:]
            print('estimated tasks: {}'.format(len(cmd)), '    [time: {}]'.format(datetime.datetime.now()))
    return c


def set_status(thread, status):
    global run_status
    run_status[str(thread)] = status


def run_cmd(thread_num):
    c = get_cmd()
    while c != '':
        with subprocess.Popen(c, stdout=subprocess.PIPE, shell=True, bufsize=1, universal_newlines=True) as p:
            for line in iter(p.stdout.readline, ''):
                set_status(thread_num, line.rstrip())
            p.wait()
        c = get_cmd()


def main(np, files):
    global cmd
    for name in files:
        cmd = read_cmd_from_file(name)

        Thread(target=status_thread, daemon=True).start()

        pool = []
        for i in range(np):
            t = Thread(target=run_cmd, args=(i,), daemon=True)
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
        start = datetime.datetime.now()
        print('start : {}'.format(start))
        main(np, files)
        finish = datetime.datetime.now()
        print('finish: {}'.format(finish))
        print('total : {}'.format(finish - start))
