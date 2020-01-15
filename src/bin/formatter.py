#!/usr/bin/env python3

from sys import exit, argv
from utils import dump_yaml, open_yaml

if __name__ == '__main__':
    try:
        if len(argv) < 2:
            raise ValueError('Not enough arguments!')

        infiles = argv[1:]

    except Exception as e:
        print(e)
        exit(1)

    for infile in infiles:
        config = open_yaml(infile)
        dump_yaml(infile, config)
