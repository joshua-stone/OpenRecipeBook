#!/usr/bin/env python3

from utils import validate_file_list
from sys import exit, argv

if __name__ == '__main__':
    try:
        if len(argv) < 3:
             raise ValueError('Not enough arguments!')

        schema, infiles = argv[1], argv[2:]

    except Exception as e:
        print(e)
        exit(1)

    if not validate_file_list(schema, infiles):
        print('Validations failed')
        exit(1)
