import pint

from . import base
from ... import materials


class MaterialStream(base.Stream):
    def __init__(self, id: str,
                 initial_fractions: dict,
                 initial_temperature: pint.Quantity,
                 use_molar_fractions=False):
        super().__init__(id)
        self.components = materials.ComponentList()

        if use_molar_fractions:
            self.components.mole_fractions = initial_fractions
        else:
            self.components.mass_fractions = initial_fractions

    def get_vapor_fraction(self):
        self.components.get_vapor_fraction(self.temperature)

    def get_liquid_fraction(self):
        self.components.get_liquid_fraction(self.temperature)

    def get_vapor_flowrate(self):
        self.components.get_vapor_flowrate(self.temperature,
                                           self.mass_flowrate)

    def get_liquid_flowrate(self):
        self.components.get_liquid_flowrate(self.temperature,
                                            self.mass_flowrate)


# Not implemented currently
class EnergyStream(base.Stream):
    def __init__(self, id: str):
        super().__init__(id)
        raise NotImplementedError
