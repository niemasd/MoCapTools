#!/usr/bin/env python3
'''
Biovision Hierarchical Data (BVH)
'''

# imports
from gzip import open as gopen
from mocaptools.common import DEFAULT_BUFSIZE, open_file

# class to represent joint nodes ("ROOT" and "JOINT") in a BVH "HIERARCHY"
class Joint:
    # initialize a `Joint` object
    def __init__(self, name, parent=None):
        # assign member variables
        self.name = name       # name of this `Joint`
        self.parent = parent   # parent of this `Joint`
        self.children = list() # children of this `Joint`
        self.offset = None     # "OFFSET" of this `Joint` as an (x, y, z) `tuple`
        self.channels = None   # "CHANNELS" of this `Joint` as a `list`

        # if this isn't the root, add it to its parent's children
        if self.parent is not None:
            self.parent.children.append(self)

# class to represent end sites ("End Site") in a BVH "HIERARCHY"
class EndSite:
    # initialize an `EndSite` object
    def __init__(self, parent):
        self.parent = parent
        self.offset = None
        self.parent.children.append(self)

# class to represent BVH files
class BVH:
    # initialize a `BVH` object by loading a BVH file
    def __init__(self, fn, buffering=DEFAULT_BUFSIZE):
        # set things up
        self.root = None         # "ROOT" joint of this BVH
        self.frame_time = None   # time duration (seconds) of a single frame in this BVH
        self.frames = list()     # `list` of frames in this BVH, where each frame is a `list` of `float`
        curr_node = None         # current `Joint` being populated
        parsing_hierarchy = None # True = "HIERARCHY" section; False = "MOTION" section
        num_frames = None        # number of frames in "MOTION" section (only used for BVH validity check)

        # parse BVH file
        with open_file(fn, mode='rt', buffering=buffering) as f:
            for line in f:
                l = line.strip()

                # skip empty lines
                if len(l) == 0:
                    continue

                # file should start with "HIERARCHY"
                elif parsing_hierarchy is None:
                    if l == 'HIERARCHY':
                        parsing_hierarchy = True
                    else:
                        raise ValueError("Invalid BVH file: %s" % fn)

                # parsing the "HIERARCHY" section
                elif parsing_hierarchy:
                    # parse "ROOT" line
                    if l.startswith('ROOT'):
                        curr_node = Joint(name=l[4:].strip())
                        self.root = curr_node

                    # parse "JOINT" line
                    elif l.startswith('JOINT'):
                        curr_node = Joint(name=l[5:].strip(), parent=curr_node)

                    # parse "End Site" line
                    elif l == 'End Site':
                        curr_node = EndSite(parent=curr_node)

                    # `{` means beginning contents of a `Joint` or `EndSite`
                    elif l == '{':
                        if curr_node is None:
                            raise ValueError("Invalid BVH file: %s" % fn)

                    # `}` means end contents of a `Joint` or `EndSite`
                    elif l == '}':
                        curr_node = curr_node.parent

                    # parse "OFFSET" line
                    elif l.startswith('OFFSET'):
                        try:
                            x, y, z = [float(v) for v in l[6:].strip().split()]
                        except:
                            raise ValueError("Invalid BVH file: %s" % fn)
                        curr_node.offset = (x, y, z)

                    # parse "CHANNELS" line
                    elif l.startswith('CHANNELS'):
                        curr_node.channels = [v.strip() for v in l[8:].strip().split()]

                    # done parsing "HIERARCHY" section; move to "MOTION" section
                    elif l == 'MOTION':
                        parsing_hierarchy = False

                    # catch-all for any "HIERARCHY" line types I haven't handled yet
                    else:
                        raise NotImplementedError("parse line in HIERARCHY section:\n%s" % l)

                # parsing the "MOTION" section
                else:
                    # parse "Frames:" line
                    if l.startswith('Frames:'):
                        num_frames = int(l[7:])

                    # parse "Frame Time:" line
                    elif l.startswith('Frame Time:'):
                        self.frame_time = float(l[11:])

                    # parse frame line
                    else:
                        self.frames.append([float(v) for v in l.strip().split()])

    # string representation of this `BVH` object
    def __str__(self):
        return "BVH file with %d frames and %ss frame time = %ss total duration" % (len(self.frames), self.frame_time, self.frame_time * len(self.frames))

    # save a `BVH` object to a file-like
    def save(self, out_file):
        # open output file if given a filename
        if isinstance(out_file, str):
            if out_file.endswith('.gz'):
                out_file = gopen(out_file, 'wt')
            else:
                out_file = open(out_file, 'w')

        # write this `BVH` to output file
        raise NotImplementedError("TODO WRITE BVH TO out_file")

        # close output file
        out_file.close()
