from yaml import safe_load
from os import walk
from os.path import join, relpath
from glob import glob
from enum import Enum, auto
from re import findall, search

class Temperature(Enum):
    Imperial = auto()
    SI = auto()

__TEMPERATURE_UNIT__ = [Temperature.Imperial]

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

def join_params(old_params, new_params):
    new_dict = dict(list(old_params.items()) + list(new_params.items()))

    return new_dict


def list_files(path, pattern):
    return [relpath(result, path) for value in walk(path) for result in glob(join(value[0], pattern))]
