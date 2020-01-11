#!/usr/bin/env python3

from utils import build_documents
from sys import argv, exit

if __name__ == '__main__':
    try:
        if len(argv) < 4:
            raise ValueError('Not enough arguments!')

        schema, *sources, destination = argv[1:]

    except Exception as e:
        print(e)
        exit(1)

    for source in sources:
        build_documents(schema, source, destination)
