""" Material Transport Unit Operation Classes

Classes
-------
Split: UnitOperation
    Material stream splitting using valve
Join: UnitOperation
    Stream mixing (ideal) at pipe joint
Compressor: UnitOperation
    Gas compressor
"""
import warnings

from . import base


class Split(base.UnitOperation):
    """Subclass of FlowSheetObject used for splitting streams.

    Attributes
    ----------
    position: float
        Value in range [0, 100] indicating percent opening of valve
        to secondary outlet.
    vrange: pint.Quantity
        Maximum flowrate of valve to secondary outlet.
    primary_outlet: MatStream
        Outlet of split with no valve present (i.e. when the valve is closed,
        all flow is directed here)
    secondary_outlet: MatStream
        Oulet of split where valve is located, changing position attribute
        affects flowrate to this stream.
    Methods
    -------

    """
    inelet = None
    primary_outlet = None
    secondary_outlet = None
    _position = 0
    vrange = 0

    def __init__(self, id: str) -> None:
        super().__init__(id)
        raise NotImplementedError

    def position() -> dict:
        doc = """Position of valve.

              Position has range of [0,100] with 0 indicating flow favoring
              primary outlet and 100 indicaing flow favoring secondary outlet.
              Values of 0 and 100 do not necessarily mean complete flow to one
              outlet.
              """

        def fget(self) -> float:
            """Returns the valve position."""
            return(self._position)

        def fset(self, value: float) -> None:
            """Sets the valve position."""
            if not isinstance(value, (int, float)):
                raise TypeError("Expected a numeric valve position")
            elif value > 100:
                warnings.warn(f"Position of valve {self.label} exceeds 100, "
                              f" setting position to 100", RuntimeWarning)
                value = 100
            elif value < 0:
                warnings.warn(f"Position of valve {self.label} is below 0, "
                              f" setting position to 0", RuntimeWarning)
                value = 0
            self._source = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    position = property(**position())


class Join(base.UnitOperation):
    """Subclass of FlowSheetObject used for mixing streams.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, id: str) -> None:
        super().__init__(id)
        raise NotImplementedError


class Compressor(base.UnitOperation):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        raise NotImplementedError
