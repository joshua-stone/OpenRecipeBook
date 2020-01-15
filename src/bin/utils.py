from yaml import safe_dump, safe_load, YAMLError
from sys import exit
import units
from cerberus import Validator, TypeDefinition
from string import Template
from os.path import splitext, basename, isfile, isdir, join
from os import listdir, mkdir
from shutil import copytree
from enum import Enum, auto
from re import findall, search

class Temperature(Enum):
    Imperial = auto()
    SI = auto()

amount_with_unit_type = TypeDefinition('amount_with_unit', (units.AmountWithUnit,), ())
Validator.types_mapping['amount_with_unit'] = amount_with_unit_type

__TEMPERATURE_UNIT__ = [Temperature.Imperial]

def set_temperature_unit(unit):
    __TEMPERATURE_UNIT__[0] = unit

def copy_directory(source, destination):
    try:
        copytree(source, destination)
    except Exception as e:
        print(e)
        exit(1)

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

def generate_includes(paths):
    includes = ['include::' + splitext(path)[0] + '.adoc[]' for path in paths]

    return '\n\n'.join(includes) + '\n'

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

def is_ref(field, value, error):
    if not any(value.startswith(item) for item in ['ref:', 'http://', 'https://']):
        error(field, 'link does not use ref syntax')

def is_time(field, value, error):
    time = value.split()
    if not len(time) == 2:
        error(field, 'time does not split into two parts')
    try:
        int(time[0])
        if not int(time[0]) > 0:
            error(field, 'time value not greater than 0')
    except ValueError:
        error(field, 'time value does not use integer')

    valid_time_units = [
        'sec',
        'second',
        'seconds',
        'min',
        'minute',
        'minutes',
        'hr',
        'hour',
        'hours',
        'day',
        'days'
    ]
    if not time[1] in valid_time_units:
        error(field, 'time unit does not appear to be valid')

def open_yaml(infile):
    try:
        with open(infile, 'r') as stream:
            config = safe_load(stream)
    except (FileNotFoundError, PermissionError, YAMLError) as e:
        print(e)
        exit(1)

    return config

def dump_yaml(infile, data):
    try:
        with open(infile, 'w') as outfile:
            outfile.write(safe_dump(data, sort_keys=False))
    except Exception as e:
        print(e)
        exit(1)

ingredient_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'name': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'products': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name':  {
                    'type': 'string',
                    'required': True,
                    'minlength': 1
                },
                'stores': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1
                            },
                            'link': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1,
                                'check_with': is_ref
                            }
                        }
                    }
                }
            }
        }
    }
}

equipment_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'name': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'products': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name':  {
                    'type': 'string',
                    'required': True,
                    'minlength': 1
                },
                'reviews': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1
                            },
                            'link': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1,
                                'check_with': is_ref
                            }
                        }
                    }
                },
                'stores': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1
                            },
                            'link': {
                                'type': 'string',
                                'required': False,
                                'minlength': 1,
                                'check_with': is_ref
                            }
                        }
                    }
                }
            }
        }
    }
}

recipe_schema = {
    'id': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'name': {
        'type': 'string',
        'required': True,
        'minlength': 1
    },
    'summary': {
        'type': 'string',
        'required': False,
        'minlength': 1
    },
    'yield': {
        'type': 'amount_with_unit',
        'required': True,
        'coerce': lambda value: units.parse_amount_with_unit(value, default_unit = 'serving')
    },
    'prep-time': {
        'type': 'string',
        'required': True,
        'minlength': 3,
        'check_with': is_time
    },
    'cook-time': {
        'type': 'string',
        'required': True,
        'minlength': 3,
        'check_with': is_time
    },
    'equipment': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name':  {
                    'type': 'string',
                    'required': True,
                    'minlength': 1
                },
                'link': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1,
                    'check_with': is_ref,
                }
            }
        }
    },
    'ingredients': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'required': True,
            'schema': {
                'name': {
                    'type': 'string',
                    'required': True
                },
                'quantity': {
                    'type': 'amount_with_unit',
                    'required': True,
                    'coerce': units.parse_amount_with_unit
                },
                'link': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1,
                    'check_with': is_ref,

                }
            }
        }
    },
    'directions': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'required': True,
            'schema': {
                'step': {
                    'type': 'string',
                    'required': True,
                    'minlength': 1,
                },
                'note': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1,
                }
            }
        }
    },
    'notes': {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'string',
            'required': False,
            'minlength': 1
        }
    }

}

def convert_ingredient(config):
    template = Template('''[[$entry_id]]
=== $entry_name
$summary
|===
| Product | Where to buy
$table
|===
''')

    entry_id = config.get('id')
    entry_name = config.get('name')

    if 'summary' in config.keys():
        summary = '\n' + config.get('summary') + '\n'
    else:
        summary = ''
    table = []
    for item in config.get('products'):
        ingredient_name = item.get('name')
        if 'stores' in item.keys():
            stores = []
            for store in item.get('stores'):
                link = generate_link(store)
                stores.append(link)

        table.append((ingredient_name, stores))

    flattened = []
    for product, links in table:
        flattened.append('| ' + product)
        flattened.append('| ' + ' +\n  '.join(links))

    output = template.safe_substitute(
        entry_id=entry_id,
        entry_name=entry_name,
        summary=summary,
        table='\n'.join(flattened)
    )
    return output

def convert_equipment(config):
    template = Template('''[[$entry_id]]
=== $entry_name
$summary
|===
| Product | Reviews | Where to buy
$table
|===
''')

    entry_id = config.get('id')
    entry_name = config.get('name')

    if 'summary' in config.keys():
        summary = '\n' + config.get('summary') + '\n'
    else:
        summary = ''
    table = []
    for item in config.get('products'):
        equipment_name = item.get('name')
        reviews = []
        stores = []
        if 'stores' in item.keys():
            for store in item.get('stores'):
                store_link = generate_link(store)
                stores.append(store_link)
                
        if 'reviews' in item.keys():
            for review in item.get('reviews'):
                review_link = generate_link(review)
                reviews.append(review_link)

        table.append([equipment_name, reviews, stores])
    flattened = []
    for (product, reviews, links) in table:
        flattened.append('| ' + product)
        flattened.append('| ' + ' +\n  '.join(reviews))
        flattened.append('| ' + ' +\n  '.join(links))

    output = template.safe_substitute(
        entry_id=entry_id,
        entry_name=entry_name,
        summary=summary,
        table='\n'.join(flattened)
    )
    return output

def convert_recipe(config):
    template = Template('''[[$entry_id]]
=== $entry_name
$summary
Yield: $entry_yield

Prep time: $prep_time

Cook time: $cook_time

Equipment:

$equipment

Ingredients:

$ingredients

Steps:

$steps
$notes
<<<
''')

    entry_id = config.get('id')
    entry_name = config.get('name')


    if 'summary' in config.keys():
        summary = '\n' + config.get('summary') + '\n'
    else:
        summary = ''

    entry_yield = f"{config.get('yield'):~g}"
    prep_time = config.get('prep-time')
    cook_time = config.get('cook-time')

    equipment = []
    for item in config.get('equipment'):
        link = generate_link(item)
        equipment.append('* ' + link)


    ingredients = []
    for item in config.get('ingredients'):
        name = item['name']

        if item['quantity'].units == units.NO_UNIT:
            text = f"{item['quantity'].magnitude:g} {name}"
        else:
            text = f"{item['quantity']:~g} of {name}"

        if 'link' in item:
            link = item['link']
            if link.startswith('ref:'):
                line = f'* <<{link[4:]}, {text}>>'
            elif link.startswith('http://') or link.startswith('https://'):
                line = f'* {link}[{text}]'
            else:
                line = f'* {text}'
        else:
            line = f'* {text}'

        ingredients.append(line)

    steps = []
    for direction in config.get('directions'):
        step = '. ' + direction['step']
        if 'note' in direction.keys():
            step += '+\n  Note: ' + direction['note']
        steps.append(generate_temperature(step))

    notes = []
    if 'notes' in config.keys():
        for note in config.get('notes'):
            notes.append('* ' + note)

    if notes:
        note_section = '\nNotes:\n\n' + '\n'.join(notes) + '\n\n'
    else:
        note_section = ''

    output = template.safe_substitute(
        entry_id=entry_id,
        entry_name=entry_name,
        entry_yield=entry_yield,
        summary=summary,
        prep_time=prep_time,
        cook_time=cook_time,
        equipment='\n'.join(equipment),
        ingredients='\n'.join(ingredients),
        steps='\n'.join(steps),
        notes=note_section
    )
    return output

schemas = {
    'ingredient': {
        'converter': convert_ingredient,
        'schema': ingredient_schema
    },
    'equipment': {
        'converter': convert_equipment,
        'schema': equipment_schema
    },
    'recipe': {
        'converter': convert_recipe,
        'schema': recipe_schema
    }
}

def schema_converter(schema):
    try:
        validator = schemas[schema]['converter']

    except Exception as e:
        print('Invalid converter!')
        exit(1)

    return validator

def schema_validator(schema):
    try:
        validator = Validator(schemas[schema]['schema'])

    except Exception as e:
        print('Invalid schema!')
        exit(1)

    return validator

def validate_file_list(schema, infiles):
    return all(map(lambda infile: validate_file(schema, infile), infiles))

def validate_file(schema, infile):
    validator = schema_validator(schema)
    config = open_yaml(infile)

    try:
        if validator.validate(config):
            print(f'File \'{infile}\' appears to be correct')

            return True
        else:
            print(validator.errors)

            return False
    except Exception as e:
        print(f'File \'{infile}\' appears to be incorrect')

        return False

def build_documents(schema, source, destination):
    validator = schema_validator(schema)
    convert = schema_converter(schema)

    basepath = basename(source)
    destination_path = join(destination, basepath)

    paths = []
    if not isdir(destination_path):
        mkdir(destination_path)

    for config in listdir(source):
        source_config = join(source, config)
        if isfile(source_config) and source_config.endswith('.yml'):
            config_data = open_yaml(source_config)
            if validator.validate(config_data):
                output_document = convert(validator.document)
                document_filename = splitext(config)[0] + '.adoc'
                document_file_destination = join(basepath, document_filename)
                with open(join(destination_path, document_filename), 'w') as out:
                    out.write(output_document)
                    paths.append(document_file_destination)
            else:
                print(f'File \'{source_config}\' is not valid: {validator.errors}')
        else:
            print('Does not appear to be either a chapter file or directory!')

        includes_data = generate_includes(paths)
        includes_destination = join(destination,  basepath + '-include.adoc')

        with open(includes_destination, 'w') as out:
            out.write(includes_data)
