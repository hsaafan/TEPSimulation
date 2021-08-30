""" Utilities

Some helper functions for flowsheet simulation.

Functions
---------
get_seed
    Grab the global seed
set_seed
    Set the global seed
get_prng
    Generate a pseduo random number using the same method as the original TEP
    simulation. Number is in the range of [-1, 1]
get_prng_pos
    Generate a pseduo random number using the same method as the original TEP
    simulation. Number is in the range of [0, 1]
get_noise
    Generate noise using a standard deviation input
import_yaml
    Import a YAML file
import_yaml_folder
    Import all YAML files from a folder
"""

import os
import yaml
from random import randint

import pint

seed = 0
tolerance = 1e-6


def get_seed() -> int:
    global seed
    set_seed((seed * 9228907) % 4294967296)
    return(seed)


def set_seed(new_seed: int) -> None:
    if new_seed is None:
        new_seed = randint(1, 1e6)
    elif type(new_seed) != int:
        raise TypeError("Seed must be a positive integer")
    elif new_seed <= 0:
        raise ValueError("Seed must be a positive integer")
    global seed
    seed = new_seed


def get_prng() -> float:
    """ Pseudo Random Number Generator

    Returns a value in the range [-1, 1]
    """
    return(2 * get_seed() / 4294967296 - 1)


def get_prng_pos() -> float:
    """ Pseudo Random Number Generator

    Returns a value in the range [0, 1]
    """
    return(get_seed() / 4294967296)


def get_noise(stdv: float) -> float:
    """ Measurment Noise

    Generates measurement noise
    """
    noise = 0
    for i in range(12):
        noise += get_prng(i)
    noise = (noise - 6) * stdv
    return(noise)


def dict_to_lowercase(dictionary: dict) -> dict:
    """ Changes all keys of a dictionary to lowercase """
    for key, val in dictionary.items():
        if type(val) is dict:
            dict_to_lowercase(val)
        if key != key.lower():
            dictionary.pop(key)
            dictionary[key.lower()] = val
            dict_to_lowercase(dictionary)
            break
    return(dictionary)


def import_yaml(path: str) -> dict:
    """
    Opens a yaml file given the path and returns a dictionary
    object containing the yaml properties.
    """
    with open(path, 'r') as stream:
        yaml_object = yaml.load(stream, Loader=yaml.SafeLoader)
    dict_to_lowercase(yaml_object)
    return(yaml_object)


def import_yaml_folder(directory: str = '/') -> dict:
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


def compare_dict_struct(first: dict, second: dict) -> bool:
    if not isinstance(first, dict) or not isinstance(second, dict):
        raise TypeError(f"Expected dict objects, got "
                        f"{type(first)} and {type(second)}")
    if first.keys() == second.keys():
        # Check children
        for key in first.keys():
            first_is_dict = isinstance(first[key], dict)
            second_is_dict = isinstance(second[key], dict)

            if first_is_dict and second_is_dict:
                return(compare_dict_struct(first[key], second[key]))
            elif first_is_dict or second_is_dict:
                # Only one is a dictionary
                return False
    else:
        return False
    return True


def pint_check(value, expected_units, no_errors: bool = False) -> bool:
    """ Error checking for a pint object

    expected_units is the dimensionality and should include the brackets, for
    example to check that a value passed is a velocity, you could pass
    '[length] / [time]' or '[velocity]'
    If no_errors has been set as True, the function will return a False value
    rather than raising an error.
    """
    if not isinstance(value, pint.Quantity):
        if no_errors:
            return(False)
        raise TypeError(f"Expected a pint Quantity object, "
                        f"got a {type(value)} instead")
    elif not value.check(expected_units):
        if no_errors:
            return(False)
        raise TypeError(f"Expected dimensionality of {expected_units}, got "
                        f"{value.dimensionality} instead")
    return(True)
