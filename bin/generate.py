#!/usr/bin/env python3

import sys
sys.path.append('lib')

from os.path import join
from helpers import list_files, open_yaml
from sys import exit
from argparse import ArgumentParser

from recipe import Recipe

def main():
    parser = ArgumentParser(description='Tool for generating recipe books')
    parser.add_argument('-i', '--infile', type=str, default='data/book.yml', help='Input file describing various editions, e.g., \'data/book.yml\'')
    parser.add_argument('-d', '--datadir', type=str, default='data')
    parser.add_argument('-t', '--temperature', help='Set temperature', choices=['imperial', 'si'], default='imperial')

    args = parser.parse_args()

    try:
        infile = args.infile
        datadir = args.datadir
        temperature = args.temperature
    except Exception as e:
        print(e)
        exit(1)

    recipe_dir = join(datadir, 'recipes')
    recipe_files = list_files(recipe_dir, '*.yml')

    for infile in recipe_files:
         data = open_yaml(join(recipe_dir, infile))
         recipe = Recipe(**data)

if __name__ == '__main__':
    main()
