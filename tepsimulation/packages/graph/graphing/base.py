""" Base classes for flowsheet graph

The flowsheet is implemented as a graph where the streams are the edges
and the unit operations are the nodes

Classes
-------
FlowSheetObject
    Base class for streams and unit operations
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
import warnings

from ... import utils


class FlowSheetObject:
    """ Generic flowsheet object class

    This class is used as a base for all flowsheet objects and handles common
    tasks.

    Attributes
    ----------
    id: str
        User set label for identifying object
    """

    def __init__(self, id: str):
        self.id = id
        self._temperature = None
        self._pressure = None

    def temperature():
        doc = """Current temperature"""

        def fget(self):
            return(self._temperature)

        def fset(self, value):
            if utils.pint_check(value, '[temperature]'):
                self._temperature = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    temperature = property(**temperature())

    def pressure():
        doc = """Current pressure"""

        def fget(self):
            return(self._pressure)

        def fset(self, value):
            if utils.pint_check(value, '[pressure]'):
                self._pressure = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    pressure = property(**pressure())


class Stream(FlowSheetObject):
    """ Stream class

    The streams are though of as the edges of a graph. These objects contain
    information about how to direct flow of material and energy. As edges, they
    only have two connections, an input and an output. For mixing and splitting
    operations, see the transport module classes. Inputs to the flowsheet and
    outputs out of the flowsheet are treated as nodes and the Inlet or Outlet
    class should be used instead.

    Attributes
    ----------
    source: UnitOperation
        The inlet of the stream
    sink: UnitOperation
        The outlet of the stream
    """

    def __init__(self, id: str):
        super().__init__(id)

    def __str__(self):
        try:
            str_repr = f"{self.id}: {self._source.id} ----> {self._sink.id}"
        except AttributeError:
            str_repr = f"{self.id}: Broken connection"
        return(str_repr)

    def pressure():
        doc = """Pressure difference of source and sink"""

        def fget(self):
            pressure_diff = self.sink.pressure - self.source.pressure
            return(pressure_diff)

        def fset(self, value):
            raise AttributeError(f"Attempted to set pressure of stream "
                                 f"{self.id}")

        return({'fget': fget, 'fset': fset, 'doc': doc})
    pressure = property(**pressure())

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


class UnitOperation(FlowSheetObject):
    """ Generic Unit Operation class

    Acts as a template for other unit operation classes but should not be used
    directly in the flowsheet.

    Attributes
    -----------
    outlets: dict
        The outlets of the unit operation
    inlets: dict
        The inlets of the unit operation

    Methods
    --------
    add_inlet
        Adds a Stream object to the unit operation inlets dictionary
    add_outlet
        Adds a Stream object to the unit operation outlets dictionary
    step
        Moves the unit operation forward by a timestep; this should not be
        overriden in child classes, override step_preprocess, step_events, or
        step_postprocess instead
    step_preprocess
        Error checking that happens before a time step occurs
    step_events
        All the events that constitute a time step. For example, a reactor
        would include reactions, temperature changes, pressure changes, etc.
        here. This should be overriden by any child classes, as it will throw
        an error otherwise.
    step_postprocess
        Cleanup operations after a step has occurred, these could be included
        in step_events instead but this is provided as a way of keeping the
        code clean
    """
    def __init__(self, id: str):
        super().__init__(id)
        self.outlets = dict()
        self.inlets = dict()
        self._temperature = None
        self._pressure = None

    def __str__(self):
        incoming = []
        outgoing = []

        for stream in self.inlets:
            incoming.append(stream.source.id)

        for stream in self.outlets:
            outgoing.append(stream.sink.id)

        return(f'{incoming} ---> {self.id} ---> {outgoing}')

    def add_inlet(self, stream: Stream, inlet_id: str = "inlet"):
        if inlet_id in self.inlets.keys():
            warnings.warn(f"{stream.id} is overwriting an inlet of {self.id}")
        self.inlets[inlet_id] = stream
        stream.sink = self

    def add_outlet(self, stream: Stream, outlet_id: str = "outlet"):
        if outlet_id in self.inlets.keys():
            warnings.warn(f"{stream.id} is overwriting an outlet of {self.id}")
        self.outlets[outlet_id] = stream
        stream.source = self

    def step_preprocess(self, time_step: pint.Quantity):
        utils.pint_check(time_step, '[time]')

    def step_events(self, time_step: pint.Quantity):
        raise NotImplementedError

    def step_postprocess(self):
        pass

    def step(self, time_step: pint.Quantity):
        self.step_preprocess(time_step)
        self.step_events(time_step)
        self.step_postprocess()


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
