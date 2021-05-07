""" Utilities

Some helper functions for flowsheet simulation.

Functions
---------
"""
__author__ = "Hussein Saafan"

import os
import yaml


def get_prng():
    """ Pseudo Random Number Generator

    Returns a value in the range [-1, 1]
    """
    seed = (seed * 9228907) % 4294967296
    ret_val = 2 * seed / 4294967296 - 1
    return(ret_val)


def get_prng_pos():
    """ Pseudo Random Number Generator

    Returns a value in the range [0, 1]
    """
    seed = (seed * 9228907) % 4294967296
    ret_val = seed / 4294967296
    return(ret_val)


def get_noise(stdv):
    """ Measurment Noise

    Generates measurement noise
    """
    noise = 0
    for i in range(12):
        noise = noise + get_prng(i)
    noise = (noise - 6) * stdv
    return(noise)


def import_yaml(path):
    """
    Opens a yaml file given the path and returns a dictionary
    object containing the yaml properties.
    """
    stream = open(path, 'r')
    yaml_object = yaml.load(stream, Loader=yaml.SafeLoader)
    return(yaml_object)


def import_yaml_folder(directory: str = '/'):
    """
    Iterates through directory and looks for yaml files,
    if one is found, it is imported and stored in a dictionary
    with its root filename (without its extension) as the key
    """
    yaml_objects = {}
    for entry in os.scandir(directory):
        if entry.name.endswith('.yaml') and entry.is_file():
            file_name = entry.name[:-5]
            yaml_properties = import_yaml(entry.path)
            yaml_objects[file_name] = yaml_properties
    return(yaml_objects)
