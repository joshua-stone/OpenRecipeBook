from yaml import safe_load, safe_dump
from os import walk, mkdir
from os.path import join, relpath
from glob import glob
from enum import Enum, auto
from re import findall, search
from os.path import join, dirname, splitext
from bookconfig import BookConfig
from datetime import timedelta

#from equipmentasciidocpresenter import EquipmentAsciidocPresenter
from cover import Cover
from chapter import Chapter

class Temperature(Enum):
    Imperial = auto()
    SI = auto()

__TEMPERATURE_UNIT__ = [Temperature.Imperial]

def parse_time(time):
    quantity, unit = time.split()

    if unit in ['s', 'sec', 'second', 'seconds']:
        return timedelta(seconds=int(quantity))
    elif unit in ['m', 'min', 'minute', 'minutes']:
        return timedelta(minutes=int(quantity))
    elif unit in ['h', 'hr', 'hour', 'hours']:
        return timedelta(hours=int(quantity))
    elif unit in ['d', 'day', 'days']:
        return timedelta(days=int(quantity))
    else:
        raise Exception('Invalid time unit')

def set_temperature_unit(unit):
    __TEMPERATURE_UNIT__[0] = unit

def cels_to_fahr(temperature):
    return f'{int(9.0/5.0 * temperature + 32)}° F'

def fahr_to_cels(temperature):
    return f'{int(5.0/9.0 * (temperature - 32))}° C'

def generate_temperature(text):
    for match in findall('\[temp:-?\d*[FfCc]\]', text):
        *value, unit = search('-?\d*[FfCc]', match)[0]
        temperature = int(''.join(value))

        if unit in ('C', 'c'):
            if __TEMPERATURE_UNIT__[0] == Temperature.SI:
                output = f'{temperature}° C'
            else:
                output = cels_to_fahr(temperature)

        elif unit in ('F', 'f'):
            if __TEMPERATURE_UNIT__[0] == Temperature.Imperial:
                output = f'{temperature}° F'
            else:
                output = fahr_to_cels(temperature)
        else:
            raise ValueError('Invalid temperature unit!')
        text = text.replace(match, output)
    return text

def ref_encode(ref):
    chars = ':/'
    for c in chars:
        ref = ref.replace(c, '_')

    return ref

def generate_link(config):
    try:
        name = config.get('name')
        if 'link' in config.keys():
            link = config.get('link')
        else:
            link = ''

        if link.startswith('ref:'):
            line = f'<<{link[4:]}, {name}>>'
        elif link.startswith('http://') or link.startswith('https://'):
            line = f'{link}[{name}]'
        else:
            line = f'{name}'
    except Exception as e:
        print(e)
        exit(1)

    return line

def open_yaml(infile):
    with open(infile, 'r') as stream:
        config = safe_load(stream)

    return config

def dump_yaml(infile, data):
    try:
        with open(infile, 'w') as outfile:
            outfile.write(safe_dump(data, sort_keys=False))
    except Exception as e:
        print(e)
        exit(1)

def join_params(old_params, new_params):
    new_dict = dict(list(old_params.items()) + list(new_params.items()))

    return new_dict


def list_files(path, pattern):
    return [relpath(result, path) for value in walk(path) for result in glob(join(value[0], pattern))]

def generate_chapter(datadir, name):
    return Chapter(config_id=f'chapter/{name}', **open_yaml(join(datadir, 'chapter', f'{name}.yml')), level=len(name.split('/')))

def generate_section(directory, namespace, template):
    config_files = sorted(list_files(directory, '*.yml'))

    sections = {}

    for infile in config_files:
        config_id = f'{namespace}:{splitext(infile)[0]}'
        data = open_yaml(join(directory, infile))
        unit = template(**data, config_id=config_id)

        section = dirname(infile)

        if not section in sections:
            sections[section] = []

        sections[section].append(unit)

    if len(sections) == 1:
        return sections['']
    else: 
        return sections

def filter_recipe(recipe, edition):
    if edition.tags:
        if not set(edition.tags).intersection(set(recipe.data['tags'])):
            print(recipe.data['tags'])
            return False
    if edition.totaltime:
        if not (parse_time(recipe.data['preptime']) + parse_time(recipe.data['cooktime'])) <= parse_time(edition.totaltime):
            return False
    return True

def filter_section(recipe_section, edition):
    filtered_recipes = {}
    for section_name, recipes in recipe_section.items():
        for recipe in recipes:
            if filter_recipe(recipe, edition):
                if not section_name in filtered_recipes:
                    filtered_recipes[section_name] = []

                filtered_recipes[section_name].append(recipe)
    return filtered_recipes

def generate_editions(recipe_section, config_file):
    config = open_yaml(config_file)
    #for edition in config['editions']:
    config = BookConfig(config)
    editions = []
    for edition in config:
        filtered_recipes = filter_section(recipe_section, edition)
        editions.append({'cover': Cover(title=edition.title, author=edition.author, email=edition.email), 'book_id': edition.book_id,'recipes': filtered_recipes})

    return editions
