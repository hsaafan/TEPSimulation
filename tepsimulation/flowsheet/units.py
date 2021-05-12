""" Flowsheet classes.

Contains classes to model aspects of flowsheet such as process units and
material streams.

Classes
-------
FlowSheetObject: class
    The base class for all flowsheet objects
MatStream: FlowSheetObject
    A material stream
UnitOperation: FlowSheetObject
    The base class for unit operations
Split: UnitOperation
    Material stream splitting using valve
Join: UnitOperation
    Stream mixing (ideal) at pipe joint
VesselJacket: UnitOperation
    A jacket that can be placed on vessels for heat exchange
Reactor: UnitOperation
    Reactor class (CSTR)
HeatExchanger: UnitOperation
    A heat exchanger
Compressor: UnitOperation
    Gas compressor
Stripper: UnitOperation
    Stripper column
VaporLiquidSperator: UnitOperation
    Vapor liquid seperator
FlowSheet: class
    The flow sheet that contains connections and initial states
"""
import warnings
import pint
from random import randint

import utils
from flowsheet.materials import Reaction

UNITREG = pint.UnitRegistry()
UNIT = UNITREG.Quantity


class FlowSheetObject:
    """ The base class for flowsheet classes.

    Attributes
    ----------
    source: FlowSheetObject or NoneType
        The source connection
    destination: FlowSheetObject or NoneType
        The destination connection
    label: str
        A short label identifying the object

    Methods
    -------
    connect
        Set the destination of the current flowsheet object. Will also set the
        source of the object to be connected to as the current object.
    """
    _source = None
    _destination = None
    label = None
    description = None

    def __init__(self, property_dict: dict):
        """
        Create a flowsheet object, usually this is only called by another more
        specific flow sheet object class constructor.
        """
        self.label = property_dict["Label"]

    def __repr__(self):
        """Returns an object representation."""
        return(f"{type(self)}<Label.{self.label}>")

    def __str__(self):
        """Returns the object label."""
        return(self.label)

    def source():
        doc = """Source connection of flow sheet object.

              The source property defines the source connection. Self
              connections are not allowed.
              """

        def fget(self):
            """Returns the connection between itself and the source."""
            return(f"{self} <--- {self._source}")

        def fset(self, value):
            """Sets the connection between itself and the source."""
            if not isinstance(value, (FlowSheetObject, type(None))):
                raise TypeError("Expected a FlowSheetObject or subclass")
            elif value is self:
                raise AttributeError("Self connections are not permitted")
            elif value is self.destination:
                raise AttributeError("Source and destination must be distinct")
            self._source = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    source = property(**source())

    def destination():
        doc = """Destination connection of flow sheet object.

              The destination property defines the destination connection. Self
              connections are not allowed.
              """

        def fget(self):
            """Returns the connection between itself and the destination."""
            return(f"{self} ---> {self._destination}")

        def fset(self, value):
            """Sets the connection between itself and the destination."""
            if not isinstance(value, (FlowSheetObject, type(None))):
                raise TypeError("Expected a FlowSheetObject or subclass")
            elif value is self:
                raise AttributeError("Self connections are not permitted")
            elif value is self.source:
                raise AttributeError("Source and destination must be distinct")
            self._destination = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    destination = property(**destination())

    def connect(self, destination: 'FlowSheetObject'):
        """
        Connect the object as the source with another flowhseet
        object as the destination.
        """
        self.destination = destination
        destination.source = self


class MatStream(FlowSheetObject):
    """Subclass of FlowSheetObject used for material flow.

    Attributes
    ----------
    mass_vapor_fraction: float
        The mass fraction of material in the stream that is a vapor.
    molar_vapor_fraction: float
        The mole fraction of material in the stream that is a vapor.
    Methods
    -------

    """
    mass_vapor_fraction = None
    molar_vapor_fraction = None

    def __init__(self, property_dict: dict):
        """Material stream constructor that just calls parent constructor"""
        super().__init__(property_dict)


class UnitOperation(FlowSheetObject):
    """Subclass of FlowSheetObject used for material flow.

    Attributes
    ----------
    temperature: pint.Quantity
        The operating temperature of the unit operation.
    Methods
    -------

    """
    _temperature = None

    def __init__(self, unit_dict: dict):
        """
        Unit operation constructor, usually this is only called by another more
        specific unit operation object class constructor.
        """
        super().__init__(unit_dict)

    def temperature():
        doc = """Unit operation operating temperature"""

        def fget(self):
            """Returns the operating temperature."""
            return(f"{self._temperature}")

        def fset(self, value):
            """Sets the operating temperature."""
            if not isinstance(value, pint.Quantity):
                raise TypeError(f"Expected a pint Quantity object, "
                                f"got a {type(value)} instead")
            elif not value.check('[temperature]'):
                raise TypeError(f"Expected a temperature value, got "
                                f"{value.dimensionality} instead")
            self._temperature = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    temperature = property(**temperature())

    def step(self, time_step: float):
        # TODO: Add dummy functions
        pass


class Split(UnitOperation):
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

    def __init__(self, property_dict: dict):
        pass

    def position():
        doc = """Position of valve.

              Position has range of [0,100] with 0 indicating flow favoring
              primary outlet and 100 indicaing flow favoring secondary outlet.
              Values of 0 and 100 do not necessarily mean complete flow to one
              outlet.
              """

        def fget(self):
            """Returns the valve position."""
            return(self._position)

        def fset(self, value: float):
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


class Join(UnitOperation):
    """Subclass of FlowSheetObject used for mixing streams.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, property_dict: dict):
        pass


class VesselJacket(UnitOperation):
    """Subclass of UnitOperation used for heat exchange with other operations.

    Attributes
    ----------
    length: pint.Quantity
        The length of the vessel jacket.
    circumference: pint.Quantity
        The circumference of the vessel jacket from vessel diameter.
    bottom_offset: pint.Quantity
        The offset of the jacket from the bottom of the vessel.
    vessel: Reactor or Stripper or VaporLiquidSeperator
        The vessel that the jacket is attached to.
    inlet: MatStream
        The jacket inlet
    outlet: MatStream
        The jacket outlet

    Methods
    -------
    attach
        Attach the jacket to a vessel and calculate circumference and
        initial heat transfer area.
    get_level
        Calculate the percent contact with the vessel liquid for heat transfer.
    exchange_heat
        Calculate heat exchange with vessel and update temperatures of both.
    """
    _length = None
    _circumference = None
    _bottom_offset = None
    vessel = None
    inlet = None
    outlet = None

    def __init__(self, inlet: MatStream, outlet: MatStream):
        """Vessel jacket constructor"""
        self.inlet = inlet
        self.outlet = outlet
        self.inlet.connect(self)
        self.connect(self.destination)

    def length():
        doc = """Vessel jacket length"""

        def fget(self):
            """Returns the jacket length."""
            return(f"{self._length}")

        def fset(self, value):
            """Sets the jacket length."""
            if not isinstance(value, pint.Quantity):
                raise TypeError(f"Expected a pint Quantity object, "
                                f"got a {type(value)} instead")
            elif not value.check('[length]'):
                raise TypeError(f"Expected a length value, got "
                                f"{value.dimensionality} instead")
            self._length = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    length = property(**length())

    def circumference():
        doc = """Unit operation operating temperature"""

        def fget(self):
            """Returns the operating temperature."""
            return(f"{self._circumference}")

        def fset(self, value):
            """Sets the operating temperature."""
            if not isinstance(value, pint.Quantity):
                raise TypeError(f"Expected a pint Quantity object, "
                                f"got a {type(value)} instead")
            elif not value.check('[length]'):
                raise TypeError(f"Expected a length value, got "
                                f"{value.dimensionality} instead")
            self._circumference = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    circumference = property(**circumference())

    def get_level(self):
        # TODO
        return

    def exchange_heat(self, vessel_temperature):
        # TODO
        return


class Reactor(UnitOperation):
    """Subclass of UnitOperation used for CSTR vessels.

    Attributes
    ----------
    diameter: pint.Quantity
        The diameter of the reactor.
    height: pint.Quantity
        The height of the vessel (assumes cylinderical shape).
    jacket: VesselJacket or NoneType
        The vessel that the jacket is attached to.
    inlets: List of MatStream
        The reactor inlets, must be edited by connecting streams to the reactor
    outlet_vapor: MatStream
        The reactor vapor outlet
    outlet_liquid: MatStream
        The reactor liquid outlet
    agitator_speed: pint.Quantity
        Current agitator speed
    _agitator: dict
        Agitator parameters
        low_limit: pint.Quantity
            Lowest speed of agitator
        high_limit: pint.Quantity
            Highest speed of agitator
        added: boolean
            Whether the agitator has been added or not

    Methods
    -------
    """
    jacket = None
    inlets = []
    outlet_vapor = None
    outlet_liquid = None
    volume = None
    _liquid_volume = None
    _liquid_level = None
    _agitator_speed = None
    _agitator = {
        "low_limit": None,
        "high_limit": None,
        "is_powered": False,
        "added": False
    }
    _reactions = {}

    def __init__(self, reactor_dict: dict):
        """Reactor constructor"""
        super().__init__(reactor_dict)
        self.import_dict(reactor_dict)

    def import_dict(self, reactor_dict: dict):
        properties = utils.import_yaml(reactor_dict["File"])
        volume = properties["Volume"]
        self.volume = UNIT(volume["val"], volume["units"])
        return

    def agitator_speed():
        doc = """Agitator speed

              The speed of the agitator, defaults to RPM units if passed a
              float instead of a pint quantity.
              """

        def fget(self):
            """Returns the agitator speed"""
            if not self._agitator.added:
                raise RuntimeError(f"No agitator set up on reactor {self}")
            if self._agitator.is_powered:
                speed = self._agitator_speed
            else:
                speed = UNIT(0, UNIT.RPM)
            return(speed)

        def fset(self, value):
            """Sets the agitator speed"""
            if not isinstance(value, (pint.Quantity, int, float)):
                raise TypeError(f"Expected a pint Quantity object, integer, or"
                                f" float but got a {type(value)} instead")
            if isinstance(value, (int, float)):
                value = UNIT(value, UNIT.rpm)

            if value.magnitude > self._agitator.high_limit.magnitude:
                warnings.warn(f"Agitator speed of {value} is above limit, "
                              f"defaulting to {self._agitator.high_limit}",
                              RuntimeWarning)
                value = self._agitator.high_limit
            elif value.magnitude < self._agitator.low_limit.magnitude:
                warnings.warn(f"Agitator speed of {value} is below limit, "
                              f"defaulting to {self._agitator.low_limit}",
                              RuntimeWarning)
                value = self._agitator.low_limit

            self._agitator_speed = value
            self._agitator.is_powered = True

        return({'fget': fget, 'fset': fset, 'doc': doc})
    agitator_speed = property(**agitator_speed())

    def source():
        doc = """Reactor inlet(s).

              The inlets of the reactor, multiple connections are allowed, but
              must be added seperately. Connections must be MatStream objects.
              """

        def fget(self):
            """Returns the inlets."""
            return(f"{self}: <--- {self.inlets}")

        def fset(self, value):
            """Adds an inlet stream to the reactor."""
            if not isinstance(value, MatStream):
                raise TypeError(f"Expected a MatStream object, "
                                f"got {type(value)} instead")
            elif value is self.outlet_liquid or value is self.outlet_vapor:
                raise AttributeError("Cannot connect a reactor as a"
                                     " destination to its outlets")
            self.inlets.append(value)

        return({'fget': fget, 'fset': fset, 'doc': doc})
    source = property(**source())

    def liquid_volume():
        doc = """Liquid Volume (m^3).

              The volume of liquid in the reactor.
              """

        def fget(self):
            """Returns the volume of liquid in the reactor."""
            return(f"{self._liquid_volume}")

        def fset(self, value):
            """Sets the volume of liquid in the reactor."""
            if not isinstance(value, pint.Quantity):
                raise TypeError(f"Expected a pint Quantity object, "
                                f"got a {type(value)} instead")
            elif not value.check('[volume]'):
                raise TypeError(f"Expected a volume value, got "
                                f"{value.dimensionality} instead")
            self._liquid_volume = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    liquid_volume = property(**liquid_volume())

    def liquid_height():
        doc = """Liquid Height (%).

              The height of the liquid as fraction of reactor height.
              """

        def fget(self):
            """Returns the height of the liquid."""
            return(f"{self._liquid_volume/self.volume}")

        def fset(self, value):
            raise AttributeError("Liquid height can't be set directly, "
                                 "set reactor liquid volume instead")

        return({'fget': fget, 'fset': fset, 'doc': doc})
    liquid_height = property(**liquid_height())

    def add_agitator(low_rpm_limit: float, high_rpm_limit: float):
        """Adds the agitator parameters to the reactor (must be floats)"""
        if self._agitator.added:
            warnings.warn(f"{self} already has an agitator", RuntimeWarning)
        self._agitator.low_limit = UNIT(low_rpm_limit, UNIT.rpm)
        self._agitator.high_limit = UNIT(high_rpm_limit, UNIT.rpm)
        self._agitator.is_powered = False
        self._agitator.added = True

    def add_reaction(self, reaction: Reaction):
        self._reactions[label] = reaction


class HeatExchanger(UnitOperation):
    pass


class Compressor(UnitOperation):
    pass


class Stripper(UnitOperation):
    pass


class FluidSeparator(UnitOperation):
    pass


class FlowSheet:
    """ Flowsheet class for organizing model

    Attributes
    ----------
    streams: dict
        A dictionary containing all streams in the flowsheet
    units: dict
        A dictionary containing all unit operations in the flowsheet
    order: list
        Contains each unit operation in 'units' and the order of this
        list determines the order of flowsheet calculation

    Methods
    -------
    import_flowsheet
        Reads the flowsheet yaml file and imports all streams and units. Calls
        import_streams and import_units methods.
    import_streams
        Adds streams as MatStream objects to flowsheet. Called by
        import_flowsheet.
    import_units
        Adds unit operations as their respective object type. Called by
        import_flowsheet.
    """
    streams = {}
    units = {}
    order = []

    def __init__(self, materials: dict, flowsheet_file: str):
        self.import_flowsheet(flowsheet_file)

    def import_streams(self, streams_dict: dict):
        """Imports a stream dictionary into a MatStream object"""
        for key in streams_dict:
            streams_dict[key]["Label"] = key
            self.streams[key] = MatStream(streams_dict[key])
        return

    def import_units(self, units_dict: dict):
        """
        Imports a dictionary of unit operations into object.
        The dictionary should have a file tag pointing to the
        yaml file with properties and any stream connections.
        """
        for unit_type in units_dict:
            for name in units_dict[unit_type]:
                units_dict[unit_type][name]["Label"] = name
                properties = units_dict[unit_type][name]
                if unit_type == "Splits":
                    unit = Split(properties)
                elif unit_type == "Joins":
                    unit = Join(properties)
                elif unit_type == "Compressors":
                    unit = Compressor(properties)
                elif unit_type == "Heat Exchangers":
                    unit = HeatExchanger(properties)
                elif unit_type == "Reactors":
                    unit = Reactor(properties)
                elif unit_type == "Separators":
                    unit = FluidSeparator(properties)
                elif unit_type == "Strippers":
                    unit = Stripper(properties)
                else:
                    warnings.warn(f"Unrecognized unit operation: {key}",
                                  SyntaxWarning)
                self.units[name] = unit
        return

    def import_order(self, order_array: list):
        """Imports the order that the flowsheet is calculated"""
        for val in order_array:
            if val not in self.units:
                raise KeyError(f"Cannot set order for {val}, no unit"
                               f" operation with that label exists")
        for val in self.units:
            if val not in order_array:
                raise KeyError(f"Unit operation {val} has not been"
                               f" included in order array")
        self.order = order_array
        return

    def import_flowsheet(self, flowsheet_file: str):
        """Imports a flowsheet yaml file into model"""
        flowsheet_dict = utils.import_yaml(flowsheet_file)
        try:
            self.import_streams(flowsheet_dict["Streams"])
            self.import_units(flowsheet_dict["Unit Operations"])
            self.import_order(flowsheet_dict["Calculation Order"])
        except KeyError as missing_key:
            raise RuntimeError(f"Missing or improperly named flowsheet"
                               f" settings header: {missing_key}")
        return

    def step(self, time_step):
        """Executes each unit in the specified order"""
        for label in self.order:
            self.units[label].step(time_step)
        return

    def output(self):
        """Returns the measured data"""
        pass
