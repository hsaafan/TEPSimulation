""" Base classes for flowsheet graph

The flowsheet is implemented as a graph where the streams are the edges
and the unit operations are the nodes

Functions
---------
pint_check
    Used for error checking to make sure that a value passed is a pint Quantity
    object of the appropriate dimensionality

Classes
-------
Stream
    Generic Stream class, acts as 'edges' of flowsheet 'graph'
UnitOperation
    Generic Unit Operation class, acts as 'nodes' of the flowsheet 'graph'
Inlet
    A special unit operation for adding materials and energy to the flowsheet
Outlet
    A special unit operation for removing materials and energy from the
    flowsheet
"""
import pint


class Stream:
    """ Stream class

    The streams are though of as the edges of a graph. These objects contain
    information about how to direct flow of material and energy. As edges, they
    only have two connections, an input and an output. For mixing and splitting
    operations, see the transport module classes. Inputs to the flowsheet and
    outputs out of the flowsheet are treated as nodes and the Inlet or Outlet
    class should be used instead.

    Attributes
    ----------
    id: str
        User set label for identifying stream
    source: UnitOperation
        The inlet of the stream
    sink: UnitOperation
        The outlet of the stream
    """

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return(f"{self._source.id} ----> {self._sink.id}")

    def source():
        doc = """Where the stream starts"""

        def fget(self):
            return(self._source)

        def fset(self, node):
            self._source = node

        return({'fget': fget, 'fset': fset, 'doc': doc})
    source = property(**source())

    def sink():
        doc = """Where the stream ends"""

        def fget(self):
            return(self._sink)

        def fset(self, node):
            self._sink = node

        return({'fget': fget, 'fset': fset, 'doc': doc})
    sink = property(**sink())


class UnitOperation:
    """ Generic Unit Operation class

    Acts as a template for other unit operation classes but should not be used
    directly in the flowsheet.

    Attributes
    -----------
    id: str
        User set label for identifying unit operation
    outlets: dict
        The outlets of the unit operation
    inlets: dict
        The inlets of the unit operation
    temperature: pint.Quantity
        The current temperature of the unit operation
    pressure: pint.Quantity
        The current pressure of the unit operation

    Methods
    --------
    add_inlet
        Adds a Stream object to the unit operation inlets dictionary
    add_outlet
        Adds a Stream object to the unit operation outlets dictionary
    step
        Template for child classes, not implemented here
    """
    def __init__(self, id: str):
        self.outlets = dict()
        self.inlets = dict()
        self._temperature = None
        self._pressure = None

        self.id = id

    def __str__(self):
        incoming = []
        outgoing = []

        for stream in self.inlets:
            incoming.append(stream.source.id)

        for stream in self.outlets:
            outgoing.append(stream.sink.id)

        return(f'{incoming} ---> {self.id} ---> {outgoing}')

    def temperature():
        doc = """Unit Operation operating temperature"""

        def fget(self):
            return(self._temperature)

        def fset(self, value):
            if pint_check(value, '[temperature]'):
                self._temperature = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    temperature = property(**temperature())

    def pressure():
        doc = """Node operating pressure"""

        def fget(self):
            return(self._pressure)

        def fset(self, value):
            if pint_check(value, '[pressure]'):
                self._pressure = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    pressure = property(**pressure())

    def add_inlet(self, stream: Stream, inlet_id: str = "inlet"):
        self.inlets[inlet_id] = stream

    def add_outlet(self, stream: Stream, outlet_id: str = "outlet"):
        self.outlets[outlet_id] = stream

    def step(self):
        raise NotImplementedError


class Inlet(UnitOperation):
    """ Flowsheet inlets class

    Any input streams to the flowsheet (e.g. feed streams) should be here

    Methods
    -------
    add_inlet
        Overrides parent method and raises an error
    """

    def __str__(self):
        outgoing = []
        for stream in self.outlets:
            outgoing.append(stream.sink.id)
        return(f'{self.id} ---> {outgoing}')

    def add_inlet(self, stream: Stream, inlet_id: str = ""):
        raise RuntimeError("Cannot add inlet streams to flowsheet inlets")


class Outlet(UnitOperation):
    """ Flowsheet outlets class

    Any outlet streams from the flowsheet (e.g. product streams) should be here

    Methods
    -------
    add_outlet
        Overrides parent method and raises an error
    """

    def __str__(self):
        incoming = []
        for stream in self.inlets:
            incoming.append(stream.source.id)
        return(f'{incoming} ---> {self.id}')

    def add_outlet(self, stream: Stream, outlet_id: str = ""):
        raise RuntimeError("Cannot add outlet streams to flowsheet outlets")


def pint_check(value, exp_units):
    """ Error checking for a pint object

    exp_units is the dimensionality and should include the brackets, for
    example to check that a value passed is a velocity, you could pass
    '[length] / [time]' or '[velocity]'
    """
    if not isinstance(value, pint.Quantity):
        raise TypeError(f"Expected a pint Quantity object, "
                        f"got a {type(value)} instead")
    elif not value.check(exp_units):
        raise TypeError(f"Expected dimensionality of {exp_units}, got "
                        f"{value.dimensionality} instead")
    return(True)
