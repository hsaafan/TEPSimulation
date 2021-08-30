import pint
import warnings

from ... import utils


class Sensor:
    """ Sensor class for taking measurements

    Attributes
    ----------
    id: str
        User set label for identifying sensor
    flowsheet: flowsheet.FlowSheet
        The flowsheet object which the sensor is used for
    target: list
        The path to the target from the flowsheet
        e.g. ['unit_operations', 'reactor', 'temperature']
    is_attached: boolean
        Has the sensor been attached to a flowsheet
    is_hooked: boolean
        Has a target been set for the sensor to track
    sensor_offset: pint.Quantity
        A constant offset added to the sensor polled value (added before
        standard deviation is taken into account)
    sensor_stdv: pint.Quantity
        Standard deviation of the sensor noise

    Methods
    -------
    hook
        Sets a target for the sensor to poll
    poll
        Get the current sensor value with measurment noise
    """
    def __init__(self, id: str) -> None:
        self.id = id
        self._flowsheet = None
        self.target = []
        self.is_attached = False
        self.is_hooked = False

        self._sensor_offset = None
        self._sensor_stdv = None

    def _sensor_value_check(self, value: pint.Quantity,
                            prop_name: str) -> None:
        if not isinstance(value, pint.Quantity):
            warnings.warn(f"{prop_name} for {self.id} has been set without "
                          f"any units, this may cause unexpected behaviour")
        elif self.poll() is not None:
            utils.pint_check(value, self.poll().dimensionality)
        else:
            warnings.warn(f"Could not check {prop_name} of {self.id} matches "
                          f"polled sensor units")

    def flowsheet() -> dict:
        doc = """The flowsheet object the sensor hooks into"""

        def fget(self):
            # Returns Flowsheet object
            return(self._flowsheet)

        def fset(self, value) -> None:
            # value must be a Flowsheet object
            self._flowsheet = value
            self.is_attached = True

        return({'fget': fget, 'fset': fset, 'doc': doc})
    flowsheet = property(**flowsheet())

    def sensor_offset() -> dict:
        doc = """Constant offset added to the value that the sensor polls"""

        def fget(self) -> pint.Quantity:
            return(self._sensor_offset)

        def fset(self, value) -> None:
            self._sensor_value_check(value, "sensor offset")
            self._sensor_offset = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    sensor_offset = property(**sensor_offset())

    def sensor_stdv() -> dict:
        doc = """Used to return the polled value with gaussian noise"""

        def fget(self) -> pint.Quantity:
            return(self._sensor_stdv)

        def fset(self, value: pint.Quantity) -> None:
            self._sensor_value_check(value, "sensor standard deviation")
            self._sensor_stdv = value

        return({'fget': fget, 'fset': fset, 'doc': doc})
    sensor_stdv = property(**sensor_stdv())

    def hook(self, target: list) -> None:
        if not self.is_attached:
            raise RuntimeError(f"Cannot hook sensor {self.id}, sensor has not "
                               f"been attached to a FlowSheet")

        polled = self.flowsheet
        # Check that the polled value actually exists
        try:
            for id in self.target:
                if isinstance(polled, dict):
                    polled = polled[id]
                else:
                    polled = getattr(polled, id)
            self.is_hooked = True
            self.target = target
        except (AttributeError, KeyError) as e:
            warnings.warn(f"Cannot hook into {id} of {target}, check that "
                          f"this attribute or key exists", SyntaxWarning)

    def poll(self) -> pint.Quantity:
        if not (self.is_attached and self.is_hooked):
            return(None)

        polled = self.flowsheet
        for id in self.target:
            if isinstance(polled, dict):
                polled = polled[id]
            else:
                polled = getattr(polled, id)

        if self.sensor_offset is not None:
            polled += self.sensor_offset
        if self.sensor_stdv is not None:
            polled += self.sensor_stdv * utils.get_prng()
        return(polled)
