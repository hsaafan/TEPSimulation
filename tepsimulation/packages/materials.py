""" Material classes

Contains classes to model material properties.

Classes
-------
Material: class
    A material
"""
import math
import os
import warnings

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

reaction_properties = {
    "name": None,
    "components": None,
    "stoichiometry": None,
    "rate order": None,
    "phase": None,
    "enthalpy": {
        "value": None,
        "units": None
    },
    "arrhenius": {
        "a": {
            "value": None,
            "units": None
        },
        "ea": {
            "value": None,
            "units": None
        }
    }
}


class Component:
    def __init__(self, path: str) -> None:
        self._properties = None
        self.name = None
        self.id = None
        self._molar_mass = None
        self._vaporization_heat = None
        self.load_file(path)

    def load_file(self, path: str) -> None:
        yaml_dict = utils.import_yaml(path)
        if not utils.compare_dict_struct(yaml_dict, component_properties):
            raise RuntimeError(f"File '{path}' missing properties, must "
                               f"have the following properties: "
                               f"{component_properties}")
        self._properties = yaml_dict
        self._set_properties()
        ComponentList.add_component(self)

    def _set_properties(self) -> None:
        self.name = self._properties["name"]
        self.id = self.name  # alias

        # Molar mass
        value = self._properties["molar mass"]["value"]
        units = self._properties["molar mass"]["units"]
        self.molar_mass = pint.Quantity(value, units)

        # Vaporization heat
        value = self._properties["vaporization heat"]["value"]
        units = self._properties["vaporization heat"]["units"]
        self.vaporization_heat = pint.Quantity(value, units)

    def molar_mass() -> dict:
        doc = """Molar mass of component"""

        def fget(self) -> pint.Quantity:
            return(self._molar_mass)

        def fset(self, value) -> None:
            if utils.pint_check(value, '[mass] / [substance]'):
                self._molar_mass = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    molar_mass = property(**molar_mass())

    def vaporization_heat() -> dict:
        doc = """Vaporization heat of component"""

        def fget(self) -> pint.Quantity:
            return(self._vaporization_heat)

        def fset(self, value):
            if utils.pint_check(value, '[energy] / [mass]'):
                self._vaporization_heat = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    vaporization_heat = property(**vaporization_heat())

    def vapor_pressure(self, temperature: pint.Quantity) -> pint.Quantity:
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

    def liquid_density(self, temperature: pint.Quantity) -> pint.Quantity:
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

    def liquid_specific_enthalpy(self,
                                 temperature: pint.Quantity) -> pint.Quantity:
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

    def gas_specific_enthalpy(self,
                              temperature: pint.Quantity) -> pint.Quantity:
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

    def liquid_specific_enthalpy_change(self,
                                        temperature:
                                        pint.Quantity) -> pint.Quantity:
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

    def gas_specific_enthalpy_change(self, temperature:
                                     pint.Quantity) -> pint.Quantity:
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


class ComponentInstance:
    def __init__(self, component, flowrate=False) -> None:
        self.properties = component
        if flowrate:
            self.mass = pint.Quantity("0 kg/hour")
        else:
            self.mass = pint.Quantity("0 kg")

    def moles() -> dict:
        doc = """Amount or rate of moles"""

        def fget(self) -> pint.Quantity:
            return(self.mass / self.properties.molar_mass)

        def fset(self, value) -> None:
            self.mass = value * self.properties.molar_mass

        return({'fget': fget, 'fset': fset, 'doc': doc})
    moles = property(**moles())


class ComponentList:
    components = []
    _list_created = False

    # Class attributes and methods
    def list_created() -> dict:
        doc = """Has any instance of this list been made"""

        def fget() -> bool:
            return(ComponentList._list_created)

        def fset(value) -> None:
            value = bool(value)
            if ComponentList.list_created and not value:
                warnings.warn("Setting this variable to False after an "
                              "instance has been created could cause "
                              "compatibility issues with previously created "
                              "instances", UserWarning)
            ComponentList._list_created = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    list_created = property(**list_created())

    def add_component(comp: Component) -> None:
        if comp.name in ComponentList.get_component_names():
            warnings.warn(f"Component {comp.name} already exists, overriding")

        elif ComponentList.list_created:
            warnings.warn("Adding new components after a ComponentList "
                          "instance has been created could cause "
                          "compatibility issues with previously created "
                          "instances", UserWarning)
        ComponentList.components.append(comp)

    def get_component(name: str) -> Component:
        for comp in ComponentList.components:
            if comp.name == name:
                return(comp)
        raise ValueError(f"Cannot find component {name}")

    def get_component_names() -> list:
        names = []
        for comp in ComponentList.components:
            names.append(comp.name)
        return(names)

    # Class instance attributes and methods
    def __init__(self, flowrate=False) -> None:
        ComponentList.list_created = True
        self._list_instance = dict()

        # Create a dictionary for each component in the list
        for obj in ComponentList.components:
            self._list_instance[obj.name] = ComponentInstance(obj, flowrate)

    def __getitem__(self, key: str) -> Component:
        try:
            component = self._list_instance[key]
        except KeyError:
            raise KeyError(f"No component called {key} has been added")
        return(component)

    def __setitem__(self, key, new_value: pint.Quantity) -> None:
        self[key]  # Attempt to acess the component to check if it exists

        is_mass = utils.pint_check(new_value, "[mass]", no_errors=True)
        is_mole = utils.pint_check(new_value, "[substance]", no_errors=True)
        is_mass_rate = utils.pint_check(new_value, "[mass] / [time]",
                                        no_errors=True)
        is_mole_rate = utils.pint_check(new_value, "[substance] / [time]",
                                        no_errors=True)

        # We check consistency with masses since we store masses and convert
        # to moles when they are requested
        if is_mass or is_mole:
            # Quantity
            self._check_unit_consistency("[mass]")
        elif is_mass_rate or is_mole_rate:
            # Flowrate
            self._check_unit_consistency("[mass] / [time]")
        else:
            raise TypeError(f"Units must be of dimensionality: "
                            f"[mass], [mass] / [time], "
                            f"[substance], or [substance] / [time]")

        if is_mole or is_mole_rate:
            new_value = new_value * self[key].properties.molar_mass
        self[key].mass = new_value

    def _check_unit_consistency(self, exp_units) -> bool:
        """
        Checks if the stored units are all of one dimensionality, normally to
        distinguish between quantities and flow rates
        """
        for obj in self._list_instance:
            if not utils.pint_check(obj["mass"], exp_units, no_errors=True):
                return(False)
        return(True)

    def fractions(frac_type: str) -> dict:
        doc = """
              Mass/mole fraction dictionary

              To set, pass an ordered collection where the first value is
              the total mass, mass flowrate, moles, or mole flowrate, and the
              second value is a dictionary where keys correspond to the
              components and the values are their mole/mass fraction.
              """

        def fget(self) -> dict:
            fractions = dict()

            total = 0
            for comp in self._list_instance:
                if frac_type == "mass":
                    total += comp.mass
                elif frac_type == "mole":
                    total += comp.moles

            for name, comp in self._list_instance.items():
                if frac_type == "mass":
                    fractions[name] = comp.mass / total
                elif frac_type == "mole":
                    fractions[name] = comp.moles / total
            return(fractions)

        def fset(self, collection) -> None:
            try:
                total = collection[0]
                fractions = collection[1]
            except IndexError:
                raise TypeError(f"Invalid {frac_type} fraction passed")

            for name, frac in fractions:
                if frac_type == "mass":
                    self[name].mass = frac * total
                elif frac_type == "mole":
                    self[name].moles = frac * total

        return({'fget': fget, 'fset': fset, 'doc': doc})
    mass_fractions = property(**fractions("mass"))
    mole_fractions = property(**fractions("mole"))


class Reaction:
    def __init__(self, path: str) -> None:
        self.name = None
        self.components = None
        self.stoich = None
        self.order = None
        self.rate_parameters = dict()
        self.phase = None
        self.enthalpy = None
        self.load_file(path)

    def load_file(self, path: str) -> None:
        yaml_dict = utils.import_yaml(path)
        if not utils.compare_dict_struct(yaml_dict, reaction_properties):
            raise RuntimeError(f"File '{path}' missing properties, must "
                               f"have the following properties: "
                               f"{reaction_properties}")
        self._properties = yaml_dict
        self._set_properties()
        ReactionList.add_reaction(self)

    def _set_properties(self) -> None:
        self.name = self._properties["name"]
        self.id = self.name  # alias

        # Reaction Stoichiometry
        self.components = self._properties["components"]
        self.stoich = self._properties["stoichiometry"]
        if len(self.components) != len(self.stoich):
            raise IndexError(f"{self.name}: Component and stoichiometry "
                             f"length must match")

        # Reaction Rates
        self.order = self._properties["rate order"]
        if len(self.components) != len(self.order):
            raise IndexError(f"{self.name}: Component and order "
                             f"length must match")
        arrhenius = self._properties["arrhenius"]
        A = arrhenius["a"]
        Ea = arrhenius["ea"]
        self.rate_parameters["A"] = Unit(A["value"], A["units"])
        self.rate_parameters["Ea"] = Unit(Ea["value"], Ea["units"])

        # Other Properties
        phase = self._properties["phase"].lower()
        if phase not in ["gas", "vapor", "vap", "liquid", "liq"]:
            raise ValueError(f"Invalid phase: {phase}")
        self.phase = phase
        H = self._properties["enthalpy"]
        self.enthalpy = Unit(H["value"], H["units"])

    def arrhenius(self, temperature: pint.Quantity) -> pint.Quantity:
        T = temperature.to(ureg.kelvin)
        A = self.rate_parameters["A"]
        Ea = self.rate_parameters["Ea"]
        k = A * math.exp(-Ea / Rg / T)
        return(k)

    def get_rxn_rate(self, temperature: pint.Quantity,
                     components: list) -> pint.Quantity:
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

    def get_component_rxn_rates(self, temperature: pint.Quantity,
                                components: list) -> dict:
        rr = self.get_rxn_rate(temperature, components)
        component_rates = {}
        for key, val in enumerate(self.components):
            component_rates[val] = self.stoich[key] * rr
        return(component_rates)


class ReactionInstance:
    def __init__(self, reaction) -> None:
        self.properties = reaction


class ReactionList:
    reactions = []
    _list_created = False

    # Class attributes and methods
    def list_created() -> dict:
        doc = """Has any instance of this list been made"""

        def fget() -> bool:
            return(ComponentList._list_created)

        def fset(value) -> None:
            value = bool(value)
            if ComponentList.list_created and not value:
                warnings.warn("Setting this variable to False after an "
                              "instance has been created could cause "
                              "compatibility issues with previously created "
                              "instances", UserWarning)
            ComponentList._list_created = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    list_created = property(**list_created())

    def add_reaction(rxn: Reaction) -> None:
        if rxn.name in ReactionList.get_reaction_names():
            warnings.warn(f"Reaction {rxn.name} already exists, overriding")

        elif ReactionList.list_created:
            warnings.warn("Adding new reactions after a ReactionList "
                          "instance has been created could cause "
                          "compatibility issues with previously created "
                          "instances", UserWarning)
        ReactionList.reactions.append(rxn)

    def get_reaction(name: str) -> Component:
        for rxn in ReactionList.reactions:
            if rxn.name == name:
                return(rxn)
        raise ValueError(f"Cannot find reaction {name}")

    def get_reaction_names() -> list:
        names = []
        for rxn in ReactionList.reactions:
            names.append(rxn.name)
        return(names)

    # Class instance attributes and methods
    def __init__(self, exclude_list: list = []) -> None:
        ReactionList.list_created = True
        self._list_instance = dict()

        # Create a dictionary for each reaction in the list
        for obj in ReactionList.reactions:
            if obj.name not in exclude_list:
                self._list_instance[obj.name] = ReactionInstance(obj)

    def __getitem__(self, key: str) -> Reaction:
        try:
            reaction = self._list_instance[key]
        except KeyError:
            raise KeyError(f"No reaction named {key} has been added")
        return(reaction)


def import_materials(directory: str = 'components/') -> None:
    for entry in os.scandir(directory):
        Component(entry)


def import_reactions(directory: str = 'reactions/') -> dict:
    for entry in os.scandir(directory):
        Reaction(entry)
