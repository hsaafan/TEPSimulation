""" Material classes

Contains classes to model material properties.

Classes
-------
Material: class
    A material
"""
import math
import os

import pint

from . import utils


ureg = pint.UnitRegistry()
Unit = ureg.Quantity

Rg = Unit(8.314, ureg.joules / ureg.mol / ureg.kelvin)

component_properties = {
    "name": None,
    "molar mass": {
        "value": None,
        "units": None
    },
    "antoines": {
        "a": None,
        "b": None,
        "c": None,
        "base": None,
        "pressure units": None,
        "temperature units": None
    },
    "liquid density": {
        "a": None,
        "b": None,
        "c": None,
        "temperature units": None,
        "density units": None
    },
    "liquid specific enthalpy": {
        "a": None,
        "b": None,
        "c": None,
        "temperature units": None,
        "enthalpy units": None
    },
    "gas specific enthalpy": {
        "a": None,
        "b": None,
        "c": None,
        "temperature units": None,
        "enthalpy units": None
    },
    "vaporization heat": {
        "value": None,
        "units": None
    }
}
component_structure = utils.get_dict_structure(component_properties)


class Component:
    def __init__(self, path: str):
        self.load_file(path)

    def load_file(self, path: str):
        yaml_dict = utils.import_yaml(path)
        for prop in component_structure:
            valid = utils.check_property_exists(yaml_dict, prop)
            if not valid:
                raise RuntimeError(f"File '{path}' missing properties, must have "
                                f"the following properties: property_structure")
        self._properties = yaml_dict
        self.name = self._properties["name"]
        ComponentList.add_component(self)

    def get_molar_mass(self):
        model = self._properties["molar mass"]
        return(ureg(model["units"]) * model["value"])

    def get_vapor_pressure(self, temperature: Unit):
        """ Vapor Pressure as calculated by Antoine's equation """
        model = self._properties["antoines"]
        T_units = model["temperature units"]
        P_units = model["pressure units"]
        base = model["base"]

        T = temperature.to(T_units).magnitude
        A = model["a"]
        B = model["b"]
        C = model["c"]

        p_vap = ureg(P_units) * base ** (A + B / (C + T))
        return(p_vap)

    def get_liquid_density(self, temperature: Unit):
        """ Liquid Density as calculated from a polynomial model """
        model = self._properties["liquid density"]
        T_units = model["temperature units"]
        rho_units = model["density units"]

        T = temperature.to(T_units).magnitude
        A = model["a"]
        B = model["b"]
        C = model["c"]

        rho_l = ureg(rho_units) * (A + (B + C * T) * T)
        return(rho_l)

    def get_liquid_specific_enthalpy(self, temperature: Unit):
        """ Liquid Specific Enthalpy as calculated from a polynomial model """
        h_model = self._properties["liquid specific enthalpy"]
        T_units = h_model["temperature units"]
        h_units = h_model["enthalpy units"]
        h_vap_model = self._properties["vaporization heat"]

        T = temperature.to(T_units).magnitude
        A = h_model["a"]
        B = h_model["b"]
        C = h_model["c"]
        h_vap = ureg(h_vap_model["units"]) * h_vap_model["value"]

        H = ureg(h_units) * ((A + (B/2 + C/3 * T) * T) * T)
        H += h_vap
        return(H)

    def get_gas_specific_enthalpy(self, temperature: Unit):
        """ Gas Specific Enthalpy as calculated from a polynomial model """
        h_model = self._properties["gas specific enthalpy"]
        T_units = h_model["temperature units"]
        h_units = h_model["enthalpy units"]
        h_vap_model = self._properties["vaporization heat"]

        T = temperature.to(T_units).magnitude
        A = h_model["a"]
        B = h_model["b"]
        C = h_model["c"]
        h_vap = ureg(h_vap_model["units"]) * h_vap_model["value"]

        H = ureg(h_units) * ((A + (B/2 + C/3 * T) * T) * T)
        H += h_vap
        return(H)

    def get_liquid_specific_enthalpy_change(self, temperature: Unit):
        """
        Liquid Specific Enthalpy Change as
        calculated from a polynomial model
        """
        h_model = self._properties["liquid specific enthalpy"]
        T_units = h_model["temperature units"]
        h_units = h_model["enthalpy units"]

        T = temperature.to(T_units).magnitude
        A = h_model["a"]
        B = h_model["b"]
        C = h_model["c"]

        h_units += " / kelvin"
        dH = ureg(h_units) * (A + (B + C * T) * T)
        return(dH)

    def get_gas_specific_enthalpy_change(self, temperature: Unit):
        """
        Gas Specific Enthalpy Change as
        calculated from a polynomial model
        """
        h_model = self._properties["gas specific enthalpy"]
        T_units = h_model["temperature units"]
        h_units = h_model["enthalpy units"]

        T = temperature.to(T_units).magnitude
        A = h_model["a"]
        B = h_model["b"]
        C = h_model["c"]

        h_units += " / kelvin"
        dH = ureg(h_units) * (A + (B + C * T) * T)
        return(dH)


class ComponentList:
    components = []
    list_created = False

    def __init__(self):
        ComponentList.list_created = True
        self._list_instance = dict()

        # Create a dictionary for each component in the list
        for obj in ComponentList.components:
            name = obj.name
            self._list_instance[name] = dict()

            self._list_instance[name]["object"] = obj
            self._list_instance[name]["mass"] = 0

    def add_component(comp: Component):
        if comp.name in ComponentList.get_component_names():
            raise Exception(f"Component {comp.name} already exists")
        elif ComponentList.list_created:
            raise RuntimeError("Cannot add new components once a "
                               "component list has been created")
        ComponentList.components.append(comp)

    def get_component(name: str):
        for comp in ComponentList.components:
            if comp.name == name:
                return(comp)
        raise ValueError(f"Cannot find component {name}")

    def get_component_names():
        names = []
        for comp in ComponentList.components:
            names.append(comp.name)
        return(names)

    def fractions(frac_type: str):
        doc = """ Mass/mole fraction dictionary """

        def fget(self):
            fractions = dict()
            for name, comp in self._list_instance.items():
                frac = comp[frac_type + " fraction"]
                fractions[name] = frac
            return(fractions)

        def fset(self, fractions: dict):
            for name, frac in fractions.items():
                if name not in ComponentList.get_component_names():
                    raise KeyError(f"Cannot set fraction for {name} "
                                   f"beacuse it cannot be found")
                elif not isinstance(frac, (float, int)):
                    raise TypeError("Fraction must be a number")
                elif frac < 0:
                    raise ValueError("Fraction cannot be negative")
                self._list_instance[name][frac_type + " fraction"] = frac

            # Check total fraction is equal to 1
            total_frac = 0
            new_fractions = fget(self)
            for name, frac in new_fractions.items():
                total_frac += frac
            if abs(total_frac - 1) > utils.tolerance:
                raise ValueError("Total fraction cannot exceed 1")

            # Update the other fraction type
            basis = 100
            total = 0
            other_fracs = dict()
            for name, frac in new_fractions.items():
                mw = ComponentList.get_component(name).get_molar_mass()
                mw = mw.to('g / mol').magnitude
                if frac_type == 'mass':
                    val = (frac * basis) / mw
                elif frac_type == 'mole':
                    val = (frac * basis) * mw
                other_fracs[name] = val
                total += val
            for name, frac in other_fracs.items():
                new_val = other_fracs[name] / total
                if frac_type == 'mass':
                    self._list_instance[name]["mole fraction"] = new_val
                elif frac_type == 'mole':
                    self._list_instance[name]["mass fraction"] = new_val

        return({'fget': fget, 'fset': fset, 'doc': doc})
    mass_fractions = property(**fractions("mass"))
    mole_fractions = property(**fractions("mole"))


class Reaction:
    label = None
    components = None
    stoich = None
    order = None
    rate_parameters = {
        "A": None,
        "Ea": None
    }
    phase = None
    enthalpy = None

    def __init__(self, reaction_dict: dict):
        self.import_dict(reaction_dict)

    def import_dict(self, reaction_dict: dict):
        # Reaction Stoichiometry
        self.label = reaction_dict["name"]
        self.components = reaction_dict["components"]
        self.stoich = reaction_dict["stoichiometry"]
        if len(self.components) != len(self.stoich):
            raise IndexError(f"{self.label}: Component and stoichiometry "
                             f"length must match")
        # Reaction Rates
        self.order = reaction_dict["rate order"]
        if len(self.components) != len(self.order):
            raise IndexError(f"{self.label}: Component and order "
                             f"length must match")
        arrhenius = reaction_dict["arrhenius"]
        A = arrhenius["a"]
        Ea = arrhenius["ea"]
        self.rate_parameters["A"] = Unit(A["val"], A["units"])
        self.rate_parameters["Ea"] = Unit(Ea["val"], Ea["units"])
        # Other Properties
        phase = reaction_dict["phase"].lower()
        if phase not in ["gas", "vapor", "vap", "liquid", "liq"]:
            raise ValueError(f"Invalid phase: {phase}")
        self.phase = phase
        H = reaction_dict["enthalpy"]
        self.enthalpy = Unit(H["val"], H["units"])

    def arrhenius(self, temperature: Unit):
        T = temperature.to(ureg.kelvin)
        A = self.rate_parameters["A"]
        Ea = self.rate_parameters["Ea"]
        k = A * math.exp(-Ea / Rg / T)
        return(k)

    def get_rxn_rate(self, temperature: Unit, components: list):
        if len(components) != len(self.components):
            raise IndexError(f"Expected {len(self.components)} values, "
                             f"recieved {len(components)}")
        k = self.arrhenius(temperature)
        rr = k
        for i in range(len(components)):
            if self.order[i] == 0:
                continue
            if not isinstance(components[i], Unit):
                raise TypeError("Expected a pint Quantity variable")
            rr *= components[i] ** self.order[i]
        return(rr)

    def get_component_rxn_rates(self, temperature: Unit, components: list):
        rr = self.get_rxn_rate(temperature, components)
        component_rates = {}
        for key, val in enumerate(self.components):
            component_rates[val] = self.stoich[key] * rr
        return(component_rates)


def import_materials(directory: str = 'components/'):
    for entry in os.scandir(directory):
        Component(entry)


def import_reactions(directory: str = 'reactions/'):
    reactions = {}
    reaction_files = utils.import_yaml_folder(directory)
    for entry in reaction_files:
        reaction_object = Reaction(reaction_files[entry])
        reactions[reaction_object.label] = reaction_object
    return(reactions)
