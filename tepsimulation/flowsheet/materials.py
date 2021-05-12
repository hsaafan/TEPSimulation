""" Material classes

Contains classes to model material properties.

Classes
-------
Material: class
    A material
"""
import math

import pint

import utils


ureg = pint.UnitRegistry()
Unit = ureg.Quantity

Rg = Unit(8.314, ureg.joules / ureg.mol / ureg.kelvin)


class Material:
    """ Material

    Stores methods and attributes that do not depend on state

    Attributes
    ----------

    Methods
    -------
    import_dict
        Set relevant properties from yaml dict (see utils.import_yaml).
    """
    label = None
    molar_mass = None
    antoines_constants = [None, None, None]
    liquid_density_constants = [None, None, None]
    liquid_specific_enthalpy_constants = [None, None, None]
    gas_specific_enthalpy_constants = [None, None, None]
    vaporization_heat = None

    def __init__(self, material_dict: dict):
        self.import_dict(material_dict)

    def import_dict(self, material_dict: dict):
        self.label = material_dict["Name"]
        self.molar_mass = material_dict["Molar Mass"]
        self.antoines_constants = (
            material_dict["Antoines A"],
            material_dict["Antoines B"],
            material_dict["Antoines C"]
        )
        self.liquid_density_constants = (
            material_dict["Liquid Density A"],
            material_dict["Liquid Density B"],
            material_dict["Liquid Density C"]
        )
        self.liquid_specific_enthalpy_constants = (
            material_dict["Liquid Specific Enthalpy A"],
            material_dict["Liquid Specific Enthalpy B"],
            material_dict["Liquid Specific Enthalpy C"]
        )
        self.gas_specific_enthalpy_constants = (
            material_dict["Gas Specific Enthalpy A"],
            material_dict["Gas Specific Enthalpy B"],
            material_dict["Gas Specific Enthalpy C"]
        )
        self.vaporization_heat = material_dict["Vaporization Heat"]
        return


class Component(Material):
    """ Component

    Stores methods and attributes that may depend on state

    Attributes
    ----------

    Methods
    -------
    """

    material = None

    def __init__(self, material: Material):
        self.material = material

    def vapor_pressure(self, temperature: Unit):
        """ Vapor Pressure

        The vapor pressure is calculated using Antoine's equation.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.antoines_constants
        p_vap = math.exp(A + B / (C + T))
        p_vap = Unit(p_vap, ureg.pascal)
        return(p_vap)

    def get_liquid_density(self, temperature: Unit):
        """ Liquid Density

        The liquid density is calculated from a polynomial fit model.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.liquid_density_constants
        MW = self.material.molar_mass
        rho_l = A + (B + C * T) * T
        rho_l = Unit(rho_l, ureg.pound / ureg.cubic_foot)
        return(rho_l)

    def get_liquid_specific_enthalpy(self, temperature: Unit):
        """ Liquid Specific Enthalpy

        The enthalpy is calculated from a polynomial fit model.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.liquid_specific_enthalpy_constants
        Hvap = self.material.vaporization_heat
        H = (A + (B/2 + C/3 * T) * T) * T + Hvap
        H = Unit(H, ureg.calorie / ureg.gram)
        return(H)

    def get_gas_specific_enthalpy(self, temperature: Unit):
        """ Gas Specific Enthalpy

        The enthalpy is calculated from a polynomial fit model.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.gas_specific_enthalpy_constants
        D = Unit(self.material.vaporization_heat,
                 ureg.british_thermal_unit / ureg.pound)
        H = (A + (B/2 + C/3 * T) * T) * T
        H = Unit(H, ureg.calorie / ureg.gram)
        H += D
        return(H)

    def get_liquid_specific_enthalpy_change(self, temperature: Unit):
        """ Liquid Specific Enthalpy Change

        The enthalpy change is calculated from a polynomial fit model.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.liquid_specific_enthalpy_constants
        dH = A + (B + C * T) * T
        dH = Unit(dH, ureg.calorie / ureg.gram / ureg.kelvin)
        return(dH)

    def get_gas_specific_enthalpy_change(self, temperature: Unit):
        """ Gas Specific Enthalpy Change

        The enthalpy change is calculated from a polynomial fit model.
        """
        T = temperature.to(ureg.celsius).magnitude
        A, B, C = self.material.gas_specific_enthalpy_constants
        dH = A + (B + C * T) * T
        dH = Unit(dH, ureg.calorie / ureg.gram / ureg.kelvin)
        return(dH)


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
        self.label = reaction_dict["Name"]
        self.components = reaction_dict["Components"]
        self.stoich = reaction_dict["Stoichiometry"]
        if len(self.components) != len(self.stoich):
            raise IndexError(f"{self.label}: Component and stoichiometry "
                             f"length must match")
        # Reaction Rates
        self.order = reaction_dict["Rate Order"]
        if len(self.components) != len(self.order):
            raise IndexError(f"{self.label}: Component and order "
                             f"length must match")
        arrhenius = reaction_dict["Arrhenius"]
        A = arrhenius["A"]
        Ea = arrhenius["Ea"]
        self.rate_parameters["A"] = Unit(A["val"], A["units"])
        self.rate_parameters["Ea"] = Unit(Ea["val"], Ea["units"])
        # Other Properties
        phase = reaction_dict["Phase"].lower()
        if phase not in ["gas", "vapor", "vap", "liquid", "liq"]:
            raise ValueError(f"Invalid phase: {phase}")
        self.phase = phase
        H = reaction_dict["Enthalpy"]
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
    materials = {}
    material_files = utils.import_yaml_folder(directory)
    for entry in material_files:
        material_object = Material(material_files[entry])
        materials[material_object.label] = material_object
    return(materials)


def import_reactions(directory: str = 'reactions/'):
    reactions = {}
    reaction_files = utils.import_yaml_folder(directory)
    for entry in reaction_files:
        reaction_object = Reaction(reaction_files[entry])
        reactions[reaction_object.label] = reaction_object
    return(reactions)


def get_new_component_dict(materials: dict):
    components = {}
    for key in materials:
        components[key] = Component(materials[key])
    return(components)


if __name__ == "__main__":
    materials = import_materials()
    reactions = import_reactions()
    components = get_new_component_dict(materials)
    T = Unit(100, ureg.celsius)
    for key, val in components.items():
        if key == "Water":
            continue
        print(f"Properties for {key}")
        print(f"H_gas:   {val.get_gas_specific_enthalpy(T):f}")
        print(f"H_liq:   {val.get_liquid_specific_enthalpy(T):f}")
        print(f"dH_gas:  {val.get_gas_specific_enthalpy_change(T).to(ureg.kilojoule / ureg.kilogram / ureg.kelvin):f}")
        print(f"dH_liq:  {val.get_liquid_specific_enthalpy_change(T).to(ureg.kilojoule / ureg.kilogram / ureg.kelvin):f}")
        print(f"rho_liq: {val.get_liquid_density(T).to(ureg.kilogram / ureg.meter ** 3):f}")
        print(f"P_vap:   {val.vapor_pressure(T):f}")
        print(f"\n\n")
    a = Unit(800, ureg.mmHg)
    rr = reactions["3D Byproduct"].get_component_rxn_rates(T, [a, a, 0])
    print(rr)
