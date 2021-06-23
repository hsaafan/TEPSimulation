import pint


class Sensor:
    """ Sensor class for taking measurements

    Attributes
    ----------
    fs_object: FlowSheetObject
        The flowsheet object that the sensor is attached to
    attr_name: str
        The name of the attribute that the sensor polls

    Methods
    -------
    setup_sensor
        Attach the sensor to a unit operation
    poll
        Get the current sensor value with measurment noise
    """
    pass
