#!/usr/bin/env python3
'''
View a BVH file
'''

# imports
from mocaptools.bvh import BVH
from sys import argv

# recursive helper function to print joint tree
def print_node(curr_node, curr_indent='', single_indent='  '):
    print('%s- %s' % (curr_indent, curr_node))
    if hasattr(curr_node, 'children'):
        child_indent = curr_indent + single_indent
        for child in curr_node.children:
            print_node(child, child_indent)

# run tools
if __name__ == "__main__":
    if len(argv) != 2 or argv[1].replace('-','').strip().lower() in {'h', 'help'}:
        print("USAGE: %s <bvh_file>" % argv[0]); exit(1)
    bvh = BVH(argv[1])
    print(bvh)
    print_node(bvh.root)
