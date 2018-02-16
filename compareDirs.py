#!/usr/bin/env python3

# MIT License

# Copyright (c) 2018 vnetmanATzohoDOTcom

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#------------------------------------------------------------------------------
# Command-line tool to compare the contents of two directories ("left" and
# "right"), and list the files that are present in one but not in the other.
#
# Two files are considered identical if their MD5 sums match. The names of the
# files are not compared, and neither are other attributes.
#------------------------------------------------------------------------------

import os
import sys
import argparse
import hashlib

def md5sum(filename):
    """Calculate the MD5 hash of the given file"""
    try:
        fh = open(filename, 'rb')
    except IOError as e:
        print('Failed to open {} : {}'.format(filename, str(e)))
        return None

    md5 = hashlib.md5()
    try:
        while True:
            data = fh.read(4096)
            if not data:
                break
            md5.update(data)
    except IOError as e:
        fh.close()
        print('Failed to read {} : {}'.format(filename, str(e)))
        return None
    
    fh.close()
    return md5.hexdigest()
############################################################

def main():
    # compareDirs.py --left <left-root> --right <right-root>

    parser = argparse.ArgumentParser(description =
                                     'Compare the contents of two directories')

    parser.add_argument("--left", required = True,
                        dest = 'left', metavar = '<left root dir>',
                        help = 'the lhs root directory')
    parser.add_argument("--right", required = True,
                        dest = 'right', metavar = '<right root dir>',
                        help = 'the rhs root directory')

    args = parser.parse_args()

    left = args.left
    right = args.right

    for dir_arg in [left, right]:
        if not os.path.isdir(dir_arg):
            print('"' + dir_arg + '" is not a directory.')
            sys.exit(-1)

    inventory = dict()

    for (dir_root, side,) in zip((left, right,),('left', 'right',)):
        for subdir, dirs, files in os.walk(dir_root):
            print('Visiting {} ...'.format(subdir), flush = True)
            for f in files:
                full_path = subdir + '/' + f
                md5_this_file = md5sum(full_path)
                if md5_this_file not in inventory:
                    inventory[md5_this_file] = list()
                this_entry = dict()
                this_entry['side'] = side
                this_entry['dir'] = subdir
                this_entry['file'] = f
                inventory[md5_this_file].append(this_entry)

    # Walk the inventory twice
    # First identify the files that are present in left but not in right
    # Then the files that are present in right but not in left

    for (this, other) in zip(('left', 'right'), ('right', 'left')):
        banner_printed = False
        for k in inventory:
            this_presence = False
            other_presence = False
            displayed_names = list()
            for e in inventory[k]:
                if e['side'] == this:
                    this_presence = True
                    displayed_names.append('{}/{}'.format(e['dir'], e['file']))
                elif e['side'] == other:
                    other_presence = True
            if this_presence and not other_presence:
                if not banner_printed:
                    banner_printed = True
                    print('{:-^70s}'.format(''))
                    print('Files present in {}, not present in {}'.
                          format(this, other))
                    print('{:-^70s}'.format(''))
                if len(displayed_names) == 1:
                    print('{}'.format(displayed_names[0]))
                else:
                    print('{} (+ {} duplicate)'.
                          format(displayed_names[0],
                                 len(displayed_names) - 1))

    # Debug: print the inventory
    # for k in inventory:
    #     print('Hash {}:'.format(k))
    #     for e in inventory[k]:
    #         print('    {}:{}  {}'.format(e['side'], e['dir'], e['file']))

    sys.exit(0)

############################################################

if __name__ == "__main__":
    main()
