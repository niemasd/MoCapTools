#!/usr/bin/env python3
'''
Biovision Hierarchical Data (BVH)
'''

# imports
from mocaptools.bvh import BVH
from sys import argv

# run tools
if __name__ == "__main__":
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <bvh_file>" % argv[0]); exit(1)
    bvh = BVH(argv[1])
