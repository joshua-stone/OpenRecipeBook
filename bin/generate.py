#!/usr/bin/env python3

import sys
sys.path.append('lib')

from os.path import join, dirname, splitext
from helpers import list_files, open_yaml
from sys import exit
from argparse import ArgumentParser

from recipe import Recipe
from recipeasciidocpresenter import RecipeAsciidocPresenter

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
    recipe_files = sorted(list_files(recipe_dir, '*.yml'))

    sections = {}

    for infile in recipe_files:
        recipe_id = f'recipe:{splitext(infile)[0]}'
        data = open_yaml(join(recipe_dir, infile))
        recipe = Recipe(**data, recipe_id=recipe_id)

        section = dirname(infile)

        if not section in sections:
            sections[section] = []

        sections[section].append(recipe)

    for section, recipes in sections.items():
        section
        for recipe in recipes:
            a = RecipeAsciidocPresenter(recipe)
            print(a.render())

if __name__ == '__main__':
    main()
