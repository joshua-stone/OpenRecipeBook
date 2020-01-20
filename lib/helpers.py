from os import walk
from os.path import join, splitext
from glob import glob

def join_params(old_params, new_params):
    new_dict = dict(list(old_params.items()) + list(new_params.items()))

    return new_dict

def list_files(path, pattern:
    return [result for value in walk(path) for result in glob(join(value[0], pattern))]
