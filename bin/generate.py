#!/usr/bin/env python3

import sys
sys.path.append('lib')

from os import mkdir
from os.path import join, dirname, splitext, isdir
from helpers import list_files, open_yaml, generate_chapter, generate_section, generate_editions
from sys import exit
from argparse import ArgumentParser

from equipment import Equipment
from recipe import Recipe
from ingredient import Ingredient
from asciidocpresenters.recipe import RecipeAsciidocPresenter
from asciidocpresenters.equipment import EquipmentAsciidocPresenter
from asciidocpresenters.ingredient import IngredientAsciidocPresenter
from asciidocpresenters.cover import CoverAsciidocPresenter
from chapter import Chapter
from asciidocpresenters.chapter import ChapterAsciidocPresenter
def main():
    parser = ArgumentParser(description='Tool for generating recipe books')
    parser.add_argument('-b', '--builddir', type=str, default='builds', help='Destination for built documents')
    parser.add_argument('-c', '--configfile', type=str, default='data/book.yml', help='Input file describing various editions, e.g., \'data/book.yml\'')
    parser.add_argument('-d', '--datadir', type=str, default='data')
    parser.add_argument('-t', '--temperature', help='Set temperature', choices=['imperial', 'si'], default='imperial')

    args = parser.parse_args()

    try:
        configfile = args.configfile
        datadir = args.datadir
        temperature = args.temperature
        builddir = args.builddir
    except Exception as e:
        print(e)
        exit(1)

    if not isdir(builddir):
        mkdir(builddir)

    recipe_dir = join(datadir, 'recipes')

    equipment_chapter = generate_chapter(datadir, 'equipment')
    recipes = generate_section(recipe_dir, 'recipe', Recipe)
    equipment = generate_section(join(datadir, 'equipment'), 'equipment', Equipment)
    ingredients = generate_section(join(datadir, 'ingredients'), 'ingredient', Ingredient)
        
    sections = generate_editions(recipes, configfile)

    for edition in sections:
        rendered_cover = CoverAsciidocPresenter(edition['cover']).render()
        rendered_equipment_chapter = ChapterAsciidocPresenter(Chapter(config_id='chapter/equipment', **open_yaml(join(datadir, 'chapter/equipment.yml')), level=2)).render()
        rendered_equipment = '\n'.join(EquipmentAsciidocPresenter(entry).render() for entry in equipment)
        rendered_ingredient_chapter = ChapterAsciidocPresenter(Chapter(config_id='chapter/ingredients', **open_yaml(join(datadir, 'chapter/ingredients.yml')), level=2)).render()
        rendered_ingredients = '\n'.join(IngredientAsciidocPresenter(ingredient).render() for ingredient in ingredients)
        rendered_recipes_chapter = ChapterAsciidocPresenter(Chapter(config_id='chapter/recipes', **open_yaml(join(datadir, 'chapter/recipes.yml')))).render()
        rendered_recipes = []
        for section, recipes in edition['recipes'].items():
            chapter_name = join('chapter', 'recipes', section)
            rendered_chapter = ChapterAsciidocPresenter(Chapter(config_id=chapter_name, **open_yaml(join(datadir, f'{chapter_name}.yml')), level=2)).render()
            rendered_recipes.append(rendered_chapter)
            rendered_recipes.append(''.join(RecipeAsciidocPresenter(recipe).render() for recipe in recipes))
        book = [
            rendered_cover,
            rendered_equipment_chapter,
            rendered_equipment,
            rendered_ingredient_chapter,
            rendered_ingredients,
            rendered_recipes_chapter,
            '\n'.join(rendered_recipes)
        ]
        fname = f"{edition['book_id']}.adoc"
        adoc_destination = join(builddir, 'asciidoc')
        if not isdir(adoc_destination):
            mkdir(adoc_destination)
        build_destination = join(adoc_destination, fname)
        with open(build_destination, 'w') as f:
            f.write('\n'.join(book))

if __name__ == '__main__':
    main()
