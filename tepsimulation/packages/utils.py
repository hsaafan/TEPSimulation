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


def get_seed():
    global seed
    set_seed((seed * 9228907) % 4294967296)
    return(seed)


def set_seed(new_seed: int):
    if new_seed is None:
        new_seed = randint(1, 1e6)
    elif type(new_seed) != int:
        raise TypeError("Seed must be a positive integer")
    elif new_seed <= 0:
        raise ValueError("Seed must be a positive integer")
    global seed
    seed = new_seed


def get_prng():
    """ Pseudo Random Number Generator

    Returns a value in the range [-1, 1]
    """
    return(2 * get_seed() / 4294967296 - 1)


def get_prng_pos():
    """ Pseudo Random Number Generator

    Returns a value in the range [0, 1]
    """
    return(get_seed() / 4294967296)


def get_noise(stdv):
    """ Measurment Noise

    Generates measurement noise
    """
    noise = 0
    for i in range(12):
        noise += get_prng(i)
    noise = (noise - 6) * stdv
    return(noise)


def dict_to_lowercase(dictionary: dict):
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


def import_yaml(path):
    """
    Opens a yaml file given the path and returns a dictionary
    object containing the yaml properties.
    """
    with open(path, 'r') as stream:
        yaml_object = yaml.load(stream, Loader=yaml.SafeLoader)
    dict_to_lowercase(yaml_object)
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


def check_property_exists(dict_to_check: dict, property_struct: list):
    """
    Uses the property_struct list to check that properties exist in
    dict_to_check.
    Examples:
        props = {"prop_a": {"prop_c": 51, "units": "C"},
                 "prop_b": {"prop_c": 25, "units": "C"}}

        check_property_exists(props, ["prop_b", "prop_c"]) -> True
        check_property_exists(props, ["prop_a", "prop_b"]) -> False
        check_property_exists(props, [["prop_a", "prop_b"], "prop_c"]) -> True
        check_property_exists(props, ["*", "prop_c"]) -> True
        check_property_exists(props, ["*", ["prop_c", "units"]]) -> True
    """
    # Check the first value in the list
    first_key = property_struct[0]
    if str(first_key) == "*":
        # Wildcard to check all keys at that level
        first_key = list(dict_to_check.keys())
    elif type(first_key) != list:
        # Treat individual values as list for more elegant code below
        first_key = [first_key]

    for key in first_key:
        try:
            if len(property_struct) == 1:
                # Last level, just check keys exist
                dict_to_check[key]
            else:
                # Go down one level, if any of these checks return false,
                # cascade return false upwards
                if not check_property_exists(dict_to_check[key],
                                             property_struct[1:]):
                    return(False)
        except KeyError:
            return(False)
    return(True)


def get_dict_structure(dictionary: dict, root: bool = True):
    structure = []
    for key, val in dictionary.items():
        if type(val) is dict:
            structure.append([key, get_dict_structure(val, False)])
        elif root:
            structure.append([key])
        else:
            structure.append(key)
    return(structure)


def pint_check(value, expected_units):
    """ Error checking for a pint object

    expected_units is the dimensionality and should include the brackets, for
    example to check that a value passed is a velocity, you could pass
    '[length] / [time]' or '[velocity]'
    """
    if not isinstance(value, pint.Quantity):
        raise TypeError(f"Expected a pint Quantity object, "
                        f"got a {type(value)} instead")
    elif not value.check(expected_units):
        raise TypeError(f"Expected dimensionality of {expected_units}, got "
                        f"{value.dimensionality} instead")
    return(True)
