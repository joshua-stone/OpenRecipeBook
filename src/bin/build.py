#!/usr/bin/env python3

from utils import build_documents, copy_directory
from os.path import isdir, join
from os import mkdir
from sys import exit, argv

if __name__ == '__main__':
    try:
        if len(argv) < 3:
             raise ValueError('Not enough arguments!')

        build_source, build_destination = argv[1], argv[2]

    except Exception as e:
        print(e)
        exit(1)

    equipment_source_directory = join(build_source, 'config', 'equipment')
    ingredient_source_directory = join(build_source, 'config', 'ingredients')
    recipe_source_directory = join(build_source, 'config', 'recipes')
    book_dir = join(build_destination, 'book')
    if not isdir(build_destination):
        mkdir(build_destination)
        copy_directory(join(build_source, 'book'), book_dir)

    recipe_sections = [
        'basics',
        'cocktails',
        'coffee'
    ]


    build_documents('equipment', equipment_source_directory, book_dir)
    build_documents('ingredient', ingredient_source_directory, book_dir)

    for section in recipe_sections:
        recipe_source = join(recipe_source_directory, section)
        build_documents('recipe', recipe_source, join(book_dir, 'recipes'))
