#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, argparse

from filters import Filters
from tree import Tree

def analyze(settings):
    start_time = time.time()

    f = Filters(settings['code'], settings['filters'])
    tree = Tree(settings['path'], f.filters(), settings['antifilters'], settings)
    tree.output()

    time_sec = time.time() - start_time
    print ("\nanalyze time : {0:2.5f}sec".format(time_sec))

def main():
    parser = argparse.ArgumentParser(description='Line Counter')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    parser.add_argument('--hide-files', action='store_true', help='hide of files in view ')
    parser.add_argument('--size-in-byte', action='store_true', help='show size in bytes')
    parser.add_argument('-p', '--path', help='path to directory with sources codes', default='.')
    parser.add_argument('-f', '--filters', nargs='*', help='list of filters', default=[], metavar='F')
    parser.add_argument('-af', '--antifilters', nargs='*', help='list of filters', default=['^\..+$'], metavar='F')

    parser.add_argument('-v', '--view', choices=['tree', 'list'], default='tree', help='set view for display output(default: %(default)s)')
    parser.add_argument('--stats', choices=['none', 'short', 'all'], default='short', help='display statistics by code (default: %(default)s)')
    parser.add_argument('-s', '--sort', choices=['name', 'line', 'size', 'ext'], default='name', help='sort of the results(default: %(default)s)')
    parser.add_argument('--folder', choices=['none', 'local', 'global', 'both'], default='none', help='print info about directory(default: %(default)s)')
    parser.add_argument('-c', '--code', nargs='+', choices=['cpp', 'c', 'cu', 'cl', 'java', 'd', 'tex', 'cmake', 'py', 'cs', 'web', 'php'], default=[], help='print info about directory(default: %(default)s)')
    
    parser.add_argument('--nocolor',  action='store_true', help="use only white/black color for display all text")

    analyze(vars(parser.parse_args()))

if __name__ == "__main__":
    main()


