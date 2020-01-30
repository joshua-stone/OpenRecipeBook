import sys
sys.path.append('lib')

import units
from cerberus import Validator, TypeDefinition
from helpers import open_yaml, dump_yaml

amount_with_unit_type = TypeDefinition('amount_with_unit', (units.AmountWithUnit,), ())
Validator.types_mapping['amount_with_unit'] = amount_with_unit_type

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

ingredient_schema = {
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
    'servings': {
        'type': 'amount_with_unit',
        'required': True,
        'coerce': lambda value: units.parse_amount_with_unit(value, default_unit = 'serving')
    },
    'preptime': {
        'type': 'string',
        'required': True,
        'minlength': 3,
        'check_with': is_time
    },
    'cooktime': {
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

schemas = {
    'ingredient': ingredient_schema,
    'equipment': equipment_schema,
    'recipe': recipe_schema
}

def schema_validator(schema):
    try:
        #print(schemas[schema])
        validator = Validator(schemas[schema])
        
    except Exception as e:
        print(e)
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
