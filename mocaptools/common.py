#!/usr/bin/env python3
'''
Functions and classes for common tasks
'''

# imports
from gzip import open as gopen
from sys import stdin, stdout

# useful constants
DEFAULT_BUFSIZE = 1048576 # 1 MB

# open a file (or file-like) and return the file (or file-like) object
def open_file(fn, mode='rt', buffering=DEFAULT_BUFSIZE):
    if fn is None:
        if 'r' in mode:
            return stdin
        else:
            return stdout
    elif fn.strip().lower().endswith('.gz'):
        return gopen(fn, mode=mode, buffering=buffering)
    else:
        return open(fn, mode=mode, buffering=buffering)
