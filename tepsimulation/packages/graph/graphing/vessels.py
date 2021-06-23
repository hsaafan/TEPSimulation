import pint

from . import base, streams
from ... import utils


class Vessel(base.UnitOperation):
    def __init__(self, id: str):
        super().__init__(id)

    def volume():
        doc = """ Vessel volume """

        def fget(self):
            """ Calculates and returns the vessel volume. """
            if self._height is None or self._diameter is None:
                raise RuntimeError("Vessel dimensions haven't been set")
            h = self._height
            d = self._diameter
            return(h * (3.14 / 4) * d ** 2)

        def fset(self, value):
            raise RuntimeError("Volume can't be set manually, use "
                               "set_dimensions method instead")

        return({'fget': fget, 'fset': fset, 'doc': doc})
    volume = property(**volume())

    def set_dimensions(self, diameter: pint.Quantity, height: pint.Quantity):
        if diameter <= 0 or height <= 0:
            raise ValueError("Negative lengths")

        if utils.pint_check(diameter, '[length]'):
            self._diameter = diameter

        if utils.pint_check(height, '[length]'):
            self._height = height


class Reactor(Vessel):
    def __init__(self, id: str):
        super().__init__(id)
        raise NotImplementedError

    def add_reaction(self):
        pass

    def _process_reactions(self):
        pass

    def step_events(self, time_step: pint.Quantity):
        # Update inlets
        for stream in self.inlets:
            pass
        # Update internals (temp, pressure, etc.)
        # Go through reactions
        for rxn in self.reactions:
            pass
        # Update outlets
        pass


class Stripper(Vessel):
    pass


class FluidSeparator(Vessel):
    pass
