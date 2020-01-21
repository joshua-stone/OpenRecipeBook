from yaml import safe_load
from os import walk
from os.path import join, relpath
from glob import glob

def open_yaml(infile):
    with open(infile, 'r') as stream:
        config = safe_load(stream)

    return config

def join_params(old_params, new_params):
    new_dict = dict(list(old_params.items()) + list(new_params.items()))

    return new_dict


def list_files(path, pattern):
    return [relpath(result, path) for value in walk(path) for result in glob(join(value[0], pattern))]
