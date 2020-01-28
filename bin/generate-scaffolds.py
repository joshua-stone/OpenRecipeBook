#!/usr/bin/env python3

from scaffold_generators.ingredient import run_ingredient_scaffold_generator
from sys import argv, exit
import sys
sys.path.append('lib')

TYPE_MAPPINGS = {
    'ingredient': run_ingredient_scaffold_generator
}

def run_scaffold_generator(type, file_name):
    if type not in TYPE_MAPPINGS:
        raise ValueError(f"Unsupported type: `{type}`.\nSupported types are: {', '.join(TYPE_MAPPINGS.keys())}.")

    TYPE_MAPPINGS.get(type)(file_name)

if __name__ == '__main__':
    try:
        if len(argv) != 3:
            raise ValueError('Syntax: generate.py [TYPE] [output-file-name]')

        type, file_name = argv[1:]
        run_scaffold_generator(type, file_name)

    except Exception as e:
        print(e)
        exit(1)
